from base64 import b64encode
from jwt import encode
from random import randbytes, randrange, choice
from string import Template


class DecoyGenerators:
    @staticmethod
    def generateKubeConfig() -> bytes:
        subs = dict()
        templ = generateTemplate("./templates/kubeconfig")
        subs["DEV_CA_DATA"] = getFakeCertificate()
        subs["STAGING_CA_DATA"] = getFakeCertificate()
        subs["PROD_CA_DATA"] = getFakeCertificate()
        subs["DEV_CLIENT_CERT"] = getFakeCertificate()
        subs["DEV_CLIENT_KEY"] = getFakeCertificate()
        subs["STAGING_CLIENT_CERT"] = getFakeCertificate()
        subs["STAGING_CLIENT_KEY"] = getFakeCertificate()
        subs["PROD_CLIENT_CERT"] = getFakeCertificate()
        subs["PROD_CLIENT_KEY"] = getFakeCertificate()
        subs["LEGACY_CLIENT_CERT"] = getFakeCertificate()
        subs["LEGACY_CLIENT_KEY"] = getFakeCertificate()
        subs["DEV_USER_TOKEN"] = getFakeJWT()
        subs["STAGING_USER_TOKEN"] = getFakeJWT()
        subs["PROD_USER_TOKEN"] = getFakeJWT()
        subs["LEGACY_USER_TOKEN"] = getFakeJWT()
        return templ.substitute(subs).encode()

    @staticmethod
    def generateAWSCredential() -> bytes:
        subs = dict()
        templ = generateTemplate("./templates/aws_credentials")
        subs["DEFAULT_ACCESS_KEY"] = "AKIA" + getRandAlnumUpper(16)
        subs["DEV_ACCESS_KEY"] = "AKIA" + getRandAlnumUpper(16)
        subs["PROD_ACCESS_KEY"] = "AKIA" + getRandAlnumUpper(16)
        subs["DEFAULT_SECRET_KEY"] = getRandomBase64(40)[:40]
        subs["DEV_SECRET_KEY"] = getRandomBase64(40)[:40]
        subs["PROD_SECRET_KEY"] = getRandomBase64(40)[:40]
        subs["DEFAULT_SESSION_TOKEN"] = getRandomBase64(randrange(400, 600))
        subs["DEV_SESSION_TOKEN"] = getRandomBase64(randrange(400, 600))
        subs["PROD_SESSION_TOKEN"] = getRandomBase64(randrange(400, 600))

        return templ.substitute(subs).encode()

    @staticmethod
    def generateAWSConfig() -> bytes:
        subs = dict()
        aws_regions = [
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "af-south-1",
            "ap-east-1",
            "ap-south-1",
            "ap-south-2",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-southeast-3",
            "ap-southeast-4",
            "ap-northeast-1",
            "ap-northeast-2",
            "ap-northeast-3",
            "ca-central-1",
            "eu-central-1",
            "eu-central-2",
            "eu-north-1",
            "eu-south-1",
            "eu-south-2",
            "eu-west-1",
            "eu-west-2",
            "eu-west-3",
            "il-central-1",
            "me-central-1",
            "me-south-1",
            "sa-east-1",
        ]
        templ = generateTemplate("./templates/aws_config")
        region = choice(aws_regions)
        subs["DEFAULT_REGION"] = region
        subs["DEV_REGION"] = region
        subs["PROD_REGION"] = region
        output = choice(["text", "json"])
        subs["DEFAULT_OUTPUT"] = output
        subs["DEV_OUTPUT"] = output
        subs["PROD_OUTPUT"] = output

        return templ.substitute(subs).encode()


def generateTemplate(path: str) -> Template:
    with open(path) as f:
        fContents = f.read()
    return Template(fContents)


def getRandomBase64(length: int) -> str:
    return b64encode(randbytes(length)).decode()


def getFakeCertificate() -> str:
    randLen = randrange(512, 1024)
    return getRandomBase64(randLen)


def getRandAlnumUpper(length: int) -> str:
    values = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    randStr = []
    for _ in range(length):
        randStr.append(choice(values))
    return "".join(randStr)


def getFakeJWT() -> str:
    return encode(
        {"content": "not a fake payload"}, getRandomBase64(20), algorithm="HS256"
    )
