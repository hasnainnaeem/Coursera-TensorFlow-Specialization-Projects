"""
    Script to split dataset into test, train, validation directories.
    For Jupyter Notebook, simply copy paste split_dataset function.
    Check split_dataset function documentation for more details.

    Written by: M. Hasnain Naeem
    Dated: 7/13/2019

"""
import sys
import os
from shutil import copyfile
import random


def print_help():
    print("Usage:")
    print("split-dataset.py source-directory destination-directory train-ratio test-ratio validation-ratio show_message")


def split_dataset(source: str, destination: str, split_ratios: dict = {"train": .8, "test": .1, "validation": .1},
                  show_messages: bool = True):
    """
    This function splits a dataset into train, test, validation directories within
    class names according to given ratios. It shuffles the data before splitting.
    ...

    Parameters
    ----------
    source : str
        path of directory containing dataset classes
    destination : str
        path of directory to store dataset classes which contain splitted data
    split_ratios : dict
        Dictionary with keys: train, test, validation
        Value of keys are ratios for splitting data
    show_messages : bool
        if True then it print details about dataset whilst splitting

    """

    assert (split_ratios["train"] + split_ratios["test"] + split_ratios["validation"]) == 1, \
        "Incorrect split ratios passed. Make sure sum of ratios == 1."

    if show_messages:
        print("Splitting according to these ratios:")
        print("----------------------------------")
        for split, ratio in split_ratios.items():
            print("\t" + split + ": " + str(ratio))
        print()

    # getting classes in dataset
    dataset_classes = os.listdir(source)

    # iterating through classes and getting files into dictionary
    dataset = {}
    for dataset_class in dataset_classes:
        # getting source class path
        class_dir = os.path.join(source, dataset_class)
        # getting paths of working files in a list
        class_dataset = []
        for filename in os.listdir(class_dir):
            file_path = os.path.join(class_dir, filename)
            # ignore corrupted files
            if os.path.getsize(file_path) > 0:
                class_dataset.append(filename)
            else:
                print(filename + " has zero size, so ignoring.")
        # shuffling before saving
        shuffled_set = random.sample(class_dataset, len(class_dataset))
        # saving files for each class in dictionary
        dataset[dataset_class] = shuffled_set

    # making folders for splitted data
    splits = ["Train", "Test", "Validation"]
    for split in splits:
        split_dir = os.path.join(destination, split)
        os.mkdir(split_dir)

    # for each class save files to train, test, validation folder
    for dataset_class in dataset_classes:

        # splitting data of each class
        train_set_len = int(len(dataset[dataset_class]) * split_ratios["train"])
        test_set_len = int(len(dataset[dataset_class]) * split_ratios["test"])
        validation_set_len = int(len(dataset[dataset_class]) * split_ratios["validation"])

        if show_messages:
            print("'" + dataset_class + "' Class Details:")
            print("----------------------------------")
            print("\tNumber of files in Training set: " + str(train_set_len))
            print("\tNumber of files in Testing set: " + str(test_set_len))
            print("\tNumber of files in Validation set: " + str(validation_set_len))
            print()

        # saving files
        for split in splits:
            class_dir = os.path.join(source, dataset_class)
            split_dir = os.path.join(destination, split)
            class_destination = os.path.join(split_dir, dataset_class)
            try:
                # making class directory within train/test/validation folder if it doesn't exist
                os.mkdir(class_destination)
            except:
                pass

            # getting files ready to copy according to the split
            if split == "Train":
                splitset = dataset[dataset_class][0: train_set_len]
            elif split == "Test":
                splitset = dataset[dataset_class][train_set_len: train_set_len + test_set_len]
            elif split == "Validation":
                splitset = dataset[dataset_class][
                           train_set_len + test_set_len: train_set_len + test_set_len + validation_set_len]

            # copying files to folder
            for file in splitset:
                src_file = os.path.join(class_dir, file)
                dest_file = os.path.join(class_destination, file)
                copyfile(src_file, dest_file)

    if show_messages:
        print("Successfuly copied files to destination folder.")

if __name__ == "__main__":
    try:
        source = sys.argv[1]
        destination = sys.argv[2]
        train_ratio = float(sys.argv[3])
        test_ratio = float(sys.argv[4])
        validation_ratio = float(sys.argv[5])
        show_messages = sys.argv[6].lower() in ["true", "yes", "1", "t"]
    except:
        print_help()

    split_ratios = {"train": train_ratio, "test": test_ratio, "validation": validation_ratio}
    split_dataset(source, destination, split_ratios, show_messages)
