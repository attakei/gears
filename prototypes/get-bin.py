import argparse
import io
import logging
import platform
import stat
import tomllib
from pathlib import Path
from typing import TypedDict
from urllib.request import urlopen

from gears.models import GearSpec, GearTarget, Workspace

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("-W", "--workspace")
parser.add_argument("spec")


class SpecDict(TypedDict):
    version: str
    description: str
    targets: dict


def make_target() -> str:
    uname = platform.uname()
    return f"{uname.system}-{uname.machine}"


def main(args: argparse.Namespace):
    def _create_target(spec: GearSpec, target: str, data) -> GearTarget:
        os_, cpu_ = target.split("-")
        return GearTarget(gear=spec, os=os_, cpu=cpu_, **data)

    ws_path = args.workspace or Path(".local")
    workspace = Workspace(root=ws_path)
    workspace.init()

    spec_path = Path(args.spec).resolve()
    spec_data: SpecDict = tomllib.loads(spec_path.read_text())
    spec = GearSpec(name=spec_path.stem,
                    description=spec_data["description"],
                    version=spec_data["version"]
                    )
    targets = {k: _create_target(spec, k, v)
               for k, v in spec_data["targets"].items()}
    logger.info(f"Gear name is '{spec.name}'")
    target_name = make_target()
    if target_name not in targets:
        logger.error(f"Gear '{spec.name} is not supported for {target_name}")
        return False
    logger.info(f"Target is {target_name}")
    target = targets[target_name]
    resp = urlopen(url=str(target.url))
    if target.archive == "zip":
        import zipfile
        content = io.BytesIO(resp.read())
        with zipfile.ZipFile(content) as zfp:
            for p in target.paths:
                dst = workspace.bin_dir / p
                dst.write_bytes(zfp.read(p))
                dst.chmod(stat.S_IXUSR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    main(args)
