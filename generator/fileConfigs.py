from typing import Callable
from .decoyGenerators import DecoyGenerators
import os

FILE_CONFIGS: dict[str, dict[str, str | dict[str, Callable[[], bytes] | str]]] = {
    "kube": {
        "directory": os.environ["HOME"] + "/.kube/",
        "files": {"/config": DecoyGenerators.generateKubeConfig},
    },
    "aws": {
        "directory": os.environ["HOME"] + "/.aws/",
        "files": {
            "/credentials": DecoyGenerators.generateAWSCredential,
            "/config": DecoyGenerators.generateAWSConfig,
        },
    },
    "azure": {
        "directory": os.environ["HOME"] + "/.azure/",
        "files": {
            "/credentials.json": DecoyGenerators.generateAzureCred,
        },
    },
    "gcloud": {
        "directory": os.environ["HOME"] + "/.gcloud/",
        "files": {
            "/application_default_credentials.json": DecoyGenerators.generateGCloudCred,
        },
    },
    "terraform": {
        "directory": os.environ["HOME"] + "/.terraform.d/",
        "files": {
            "/credentials.tfrc.json": DecoyGenerators.generateTFCred,
        },
    },
    "docker": {
        "directory": os.environ["HOME"] + "/.docker/",
        "files": {
            "/config.json": DecoyGenerators.generateDockerConfig,
        },
    },
    "bitcoin": {
        "directory": os.environ["HOME"] + "/.bitcoin",
        "files": {
            "/bitcoin.conf": DecoyGenerators.generateBitcoinConfig,
            "/cold_wallet.dat": DecoyGenerators.generateBitcoinWallet,
            "/hot_wallet.dat": DecoyGenerators.generateBitcoinWallet,
            "/trading_wallet.dat": DecoyGenerators.generateBitcoinWallet,
        },
    },
}
