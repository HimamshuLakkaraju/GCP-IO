from gcpio.gdrive import Gdrive
from torch.utils.data import Dataset, DataLoader, BatchSampler, SequentialSampler
import cProfile
import pstats
from PIL import Image
import torchvision.transforms as T
import torch
from torchvision.utils import save_image, make_grid

# Running with a profiler to check the performance.
def run_gdrive(folder_id, batch=20, skip_labels=True):
    file_name_dict = {
        "1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg": "20imagesdataset",
        "1uBJpmFM_6CLC0AUTr6ItW8zOo5pZsF1w": "10kimagesdataset",
    }

    with cProfile.Profile() as pr:
        batch_size = batch
        g = Gdrive()
        dataset = g.create_dataset(
            data_folder_id=folder_id,
            labels_folder_id=folder_id,
            page_size=1000,
            data_file_type="image/png",
            labels_file_type="text/csv",
            skip_labels=skip_labels,
        )
        print(f"length of dataset: {len(dataset)}")
        dataloader = DataLoader(
            dataset,
            batch_size,
            sampler=BatchSampler(
                SequentialSampler(dataset), batch_size=batch_size, drop_last=True
            ),
            # collate_fn=None,
        )
        # Generating samples from the dataloader
        samples = next(iter(dataloader))

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(
            filename=f"./profiling/Gdrive_profiling_{file_name_dict[folder_id]}.prof"
        )
    images = []
    for i in range(len(samples)):
        # ignoring labels and collecting images only for verification
        img, _ = samples[i]
        images.append(img)
    images = torch.cat(images)

    grid = make_grid(images, nrow=20)
    save_image(grid, f"./examples/{file_name_dict[folder_id]}_generated_images.png")


# https://drive.google.com/drive/folders/1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg?usp=sharing
# Running for a sample dataset containing 20 images with batch size as 20
run_gdrive("1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg", 20)

# https://drive.google.com/drive/folders/1uBJpmFM_6CLC0AUTr6ItW8zOo5pZsF1w?usp=sharing
# Running for a sample dataset containing 10,000 images with batch size as 30
run_gdrive("1uBJpmFM_6CLC0AUTr6ItW8zOo5pZsF1w", 30)
