from typing import Callable
from .decoyGenerators import DecoyGenerators
import os

FILE_CONFIGS: dict[str, dict[str, str | dict[str, Callable[[], bytes] | str]]] = {
    "kube": {
        "directory": os.environ["HOME"] + "/.kube/",
        "files": {"~/.kube/config": DecoyGenerators.generateKubeConfig},
    },
    "aws": {
        "directory": os.environ["HOME"] + "/.aws/",
        "files": {
            os.environ["HOME"]
            + "/.aws/credentials": DecoyGenerators.generateAWSCredential,
            os.environ["HOME"] + "/.aws/config": DecoyGenerators.generateAWSConfig,
        },
    },
    "azure": {
        "directory": os.environ["HOME"] + "/.azure/",
        "files": {
            os.environ["HOME"]
            + "/.azure/credentials.json": DecoyGenerators.generateAzureCred,
        },
    },
    "gcloud": {
        "directory": os.environ["HOME"] + "/.gcloud/",
        "files": {
            os.environ["HOME"]
            + "/.gcloud/application_default_credentials.json": DecoyGenerators.generateGCloudCred,
        },
    },
    "terraform": {
        "directory": os.environ["HOME"] + "/.terraform.d/",
        "files": {
            os.environ["HOME"]
            + "/.terraform.d/credentials.tfrc.json": DecoyGenerators.generateTFCred,
        },
    },
    "docker": {
        "directory": os.environ["HOME"] + "/.docker/",
        "files": {
            os.environ["HOME"]
            + "/.docker/config.json": DecoyGenerators.generateDockerConfig,
        },
    },
    "bitcoin": {
        "directory": os.environ["HOME"] + "/.bitcoin",
        "files": {
            os.environ["HOME"]
            + "/.bitcoin/bitcoin.conf": DecoyGenerators.generateBitcoinConfig,
            os.environ["HOME"]
            + "/.bitcoin/cold_wallet.dat": DecoyGenerators.generateBitcoinWallet,
            os.environ["HOME"]
            + "/.bitcoin/hot_wallet.dat": DecoyGenerators.generateBitcoinWallet,
            os.environ["HOME"]
            + "/.bitcoin/trading_wallet.dat": DecoyGenerators.generateBitcoinWallet,
        },
    },
}
