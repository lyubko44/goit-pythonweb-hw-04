import asyncio
import os
import shutil
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def copy_file(file_path, output_folder):
    ext = file_path.suffix[1:]
    target_folder = output_folder / ext
    target_folder.mkdir(parents=True, exist_ok=True)
    target_path = target_folder / file_path.name
    try:
        shutil.copy(file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logger.error(f"Error copying {file_path} to {target_path}: {e}")

async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))
    await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser(description="Sort files by extension")
    parser.add_argument("source_folder", type=Path, help="Source folder to read files from")
    parser.add_argument("output_folder", type=Path, help="Output folder to store sorted files")
    args = parser.parse_args()

    await read_folder(args.source_folder, args.output_folder)

if __name__ == "__main__":
    asyncio.run(main())