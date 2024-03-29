#!/usr/bin/env python

import argparse
import datetime
import json
import os
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from textwrap import dedent

import yaml

import MAIAKubeGate
from MAIAKubeGate.helm_values import read_config_dict_and_generate_helm_values_dict
from MAIAKubeGate.kaniko import create_config_map_from_data

version = MAIAKubeGate.__version__

TIMESTAMP = "{:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

DESC = dedent(
    """
    Script to deploy the MAIAKubeGate helm chart to a Kubernetes cluster. The target cluster is specified by setting ``KUBECONFIG``
    as an environment variable, while the configuration file for the chart is specified with ``config_file``.
    """  # noqa: E501
)
EPILOG = dedent(
    """
    Example call:
    ::
        {filename}  --config-file /PATH/TO/config_file.json
    """.format(  # noqa: E501
        filename=Path(__file__).stem
    )
)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def get_arg_parser():
    pars = ArgumentParser(description=DESC, epilog=EPILOG, formatter_class=RawTextHelpFormatter)

    pars.add_argument(
        "--config-file",
        type=str,
        required=True,
        help="JSON configuration file used to generate the custom values used in the Helm chart.",
    )

    pars.add_argument(
        "--print-helm-values-only",
        type=str,
        required=False,
        help="Flag to save the generated Helm values on the specified file and exit.",
    )

    pars.add_argument(
        "--deploy-on-karmada",
        type=str2bool,
        required=False,
        default="true",
        help="Flag to set if the chart is deployed on Karmada ( Cluster Federation). Default is true.",
    )

    pars.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)

    return pars


def main():
    parser = get_arg_parser()

    arguments = vars(parser.parse_args())

    config_file = arguments["config_file"]

    with open(config_file) as json_file:
        config_dict = json.load(json_file)

    kubeconfig = yaml.safe_load(Path(os.environ["KUBECONFIG"]).read_text())

    sshProcess = subprocess.Popen(["sh"],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True,
                                  bufsize=0)

    helm_dict = read_config_dict_and_generate_helm_values_dict(config_dict, kubeconfig)

    if arguments["print_helm_values_only"]:
        print(helm_dict)
        with open(arguments["print_helm_values_only"], "w") as f:
            yaml.dump(helm_dict, f)
        return

    set_cluster = ""
    for idx, cluster in enumerate(config_dict["clusters"]):
        set_cluster += ",clusters[{}]={}".format(idx, cluster)

    if arguments["deploy_on_karmada"]:
        create_config_map_from_data(yaml.dump(helm_dict),
                                    "{}-values".format(config_dict["chart_name"].lower()),
                                    config_dict["namespace"],
                                    kubeconfig,
                                    )

        chart_url = "https://simonebendazzoli93.github.io/MAIAKubeGate/"  # TODO set this as a customizable parameter
        chart_name = "maiakubegate"  # TODO set this as a customizable parameter
        chart_version = "1.0.1"  # TODO set this as a customizable parameter

        sshProcess.stdin.write(
            "helm upgrade --install {} --namespace={} maiakubegate/hive-deploy --set chart_url={},chart_name={},chart_version={},config_map={}{}\n".format(
                config_dict["chart_name"],
                config_dict["namespace"],
                chart_url,
                chart_name,
                chart_version,
                "{}-values".format(config_dict["chart_name"].lower(),
                                   ),
                set_cluster
            ))
    else:
        with open("./values.yaml", "w") as f:  # TODO: remove this and load values from memory
            yaml.dump(helm_dict, f)

        sshProcess.stdin.write(
            "helm upgrade --install {} --namespace={} maiakubegate/maiakubegate --values ./values.yaml\n".format(
                config_dict["chart_name"], config_dict["namespace"]))

    sshProcess.stdin.close()
    for line in sshProcess.stdout:
        if line == "END\n":
            break
        print(line, end="")


if __name__ == "__main__":
    main()
