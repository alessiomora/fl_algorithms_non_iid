import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


def remove_list_from_list(orig_list, to_remove):
    new_list = []
    for element in orig_list:
        if element not in to_remove:
            new_list.append(element)
    return new_list

def load_selected_clients_statistics(selected_clients, alpha, dataset):
    path = os.path.join(dataset+"_dirichlet", str(round(alpha, 2)), "distribution.npy")
    smpls_loaded = np.load(path)
    # print(smpls_loaded)
    local_examples = np.sum(smpls_loaded, axis=1) #20
    # print(local_examples)
    return local_examples[selected_clients.tolist()]

def load_stl10_dataset_from_files(num_examples, seed=None):
    """Loads the stl10 dataset from file. Then take the first num_examples examples
    and return them in a batched dataset."""
    path = "/home/amora/pycharm_projects/flower_distillation/stl_resized"
    loaded_stl10 = tf.data.experimental.load(
        path=os.path.join(path, "stl_shuffled_" + str(seed)), element_spec=None, compression=None,
        reader_func=None
    )
    loaded_stl10 = loaded_stl10.take(num_examples)
    # loaded_stl10 = loaded_stl10.batch(batch_size)
    # print("---example--")
    # iterator = iter(loaded_stl10)
    # img, label = next(iterator)
    # print(img)
    return loaded_stl10


def load_stl10_dataset(num_examples, seed=None):
    """Loads the stl10 dataset. Resize, preprocess and shuffle the images.
     Then take the first num_examples examples and return them in dataset."""

    stl = tfds.load("stl10")
    stl_unlabelled_data = stl["unlabelled"]

    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    stl_resized = stl_unlabelled_data.map(
        lambda element: (norm_layer(tf.cast(tf.image.resize(element["image"], [32, 32]), tf.float32) / 255.0),
                         element["label"]))

    stl_resized = stl_resized.shuffle(buffer_size=100000, seed=seed, reshuffle_each_iteration=False)
    stl_resized = stl_resized.take(num_examples)

    # print("---example--")
    # iterator = iter(stl_resized)
    # img, label = next(iterator)
    # print(img)
    return stl_resized

def load_client_datasets_from_files(dataset, sampled_client, batch_size, alpha=100.0):
    """Loads a random client partition the cifar10 dataset from file.
        Examples are preprocessed via normalization layer.
        Returns a batched dataset."""

    path = os.path.join(dataset+"_dirichlet", str(round(alpha, 2)), "train")

    loaded_ds_train = tf.data.experimental.load(
        path=os.path.join(path, str(sampled_client)), element_spec=None, compression=None, reader_func=None
    )

    def element_fn_norm(image, label):
        norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                                   variance=[np.square(0.2023),
                                                             np.square(0.1994),
                                                             np.square(0.2010)])
        return norm_layer(tf.cast(image, tf.float32) / 255.0), label

    return loaded_ds_train.map(element_fn_norm).shuffle(1024).batch(
        batch_size, drop_remainder=False)

def load_client_cifar10_datasets_from_files(sampled_client, batch_size, alpha=100.0):
    """Loads a random client partition the cifar10 dataset from file.
    Examples are preprocessed via normalization layer.
    Returns a batched dataset."""

    path = os.path.join("cifar10_dirichlet", str(round(alpha, 2)), "train")

    loaded_ds_train = tf.data.experimental.load(
        path=os.path.join(path, str(sampled_client)), element_spec=None, compression=None, reader_func=None
    )

    # print(loaded_ds_train)
    def element_fn(image, label):
        return tf.cast(image, tf.float32) / 255.0, label

    def element_fn_norm(image, label):
        norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                                   variance=[np.square(0.2023),
                                                             np.square(0.1994),
                                                             np.square(0.2010)])
        return norm_layer(tf.cast(image, tf.float32) / 255.0), label

    return loaded_ds_train.map(element_fn_norm).shuffle(1024).batch(
        batch_size, drop_remainder=False)


def load_svhn_dataset(num_examples, seed=None):
    """Loads the svhn dataset. Then take the first num_examples examples
    and return them in a batched dataset."""

    # 73257 digits for training
    # 26032 digits for testing
    # 531131 digits for extras
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    svhn_tfds = tfds.load("svhn_cropped")
    svhn_train = svhn_tfds["train"]
    svhn_test = svhn_tfds["test"]

    svhn = svhn_test.concatenate(svhn_train)

    svhn = svhn.shuffle(73257 + 26032, seed=seed, reshuffle_each_iteration=False)
    svhn = svhn.take(num_examples)
    svhn = svhn.map(
        lambda element: (norm_layer(tf.cast(element["image"], tf.float32) / 255.0),
                         element["label"]))
    return svhn


def load_cifar10_dataset(num_examples, seed=None):
    """Loads the cifar10 dataset. Then take the first num_examples examples
    and return them in a batched dataset."""

    # 50000 digits for training
    # 10000 digits for testing
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    cifar10_tfds = tfds.load("cifar10")
    cifar10_train = cifar10_tfds["train"]
    cifar10_test = cifar10_tfds["test"]

    cifar10 = cifar10_test.concatenate(cifar10_train)

    cifar10 = cifar10.shuffle(60000, seed=seed, reshuffle_each_iteration=False)
    if num_examples > 60000:
        cifar10 = cifar10.take(60000)
    else:
        cifar10 = cifar10.take(num_examples)

    cifar10 = cifar10.map(
        lambda element: (norm_layer(tf.cast(element["image"], tf.float32) / 255.0),
                         element["label"]))
    return cifar10

def load_cifar100_dataset(num_examples, seed=None):
    """Loads the cifar10 dataset. Then take the first num_examples examples
    and return them in a batched dataset."""

    # 50000 digits for training
    # 10000 digits for testing
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    cifar100_tfds = tfds.load("cifar100")
    cifar100_train = cifar100_tfds["train"]
    cifar100_test = cifar100_tfds["test"]

    cifar100 = cifar100_test.concatenate(cifar100_train)

    cifar100 = cifar100.shuffle(60000, seed=seed, reshuffle_each_iteration=False)
    if num_examples > 60000:
        cifar100 = cifar100.take(60000)
    else:
        cifar100 = cifar100.take(num_examples)

    cifar100 = cifar100.map(
        lambda element: (norm_layer(tf.cast(element["image"], tf.float32) / 255.0),
                         element["label"]))
    return cifar100


def load_stanford_online_products_dataset(num_examples, seed=None):
    """Loads the stanford_online_products dataset. Then take the first num_examples examples
    and return them in a batched dataset."""

    # test	60502
    # train	59551
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    sop_tfds = tfds.load("stanford_online_products")
    sop_train = sop_tfds["train"]
    sop_test = sop_tfds["test"]

    sop = sop_test.concatenate(sop_train)

    sop = sop.shuffle(60000, seed=seed, reshuffle_each_iteration=False)
    sop = sop.take(num_examples)
    sop = sop.map(lambda element: (norm_layer(tf.cast(tf.image.resize(element["image"], [32, 32]), tf.float32) / 255.0),
                                   element["class_id"]))
    return sop


def load_dtd_dataset(num_examples, seed=None):
    """Loads the stanford_online_products dataset. Then take the first num_examples examples
    and return them in a batched dataset."""

    # test	1880
    # train	1880
    # val   1880
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    dtd_tfds = tfds.load("dtd")
    dtd_train = dtd_tfds["train"]
    dtd_test = dtd_tfds["test"]
    dtd_val = dtd_tfds["validation"]

    dtd = dtd_val.concatenate(dtd_test).concatenate(dtd_train)

    dtd = dtd.shuffle(1880*3, seed=seed, reshuffle_each_iteration=False)
    dtd = dtd.take(num_examples)
    dtd = dtd.map(lambda element: (norm_layer(tf.cast(tf.image.resize(element["image"], [32, 32]), tf.float32) / 255.0),
                                   element["label"]))
    return dtd


def load_random_dataset(num_examples, seed=None):
    """To be implemented"""
    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])
    tf.random.set_seed(1234)
    random_imgs = tf.random.uniform(shape=[100000, 32, 32, 3], minval=0, maxval=1.0, seed=1)
    random_ds = tf.data.Dataset.from_tensor_slices(random_imgs)
    random_ds = random_ds.map(lambda element: (norm_layer(element), -1) )
    random_ds = random_ds.shuffle(50000, seed=seed, reshuffle_each_iteration=False)
    random_ds = random_ds.take(num_examples)
    return random_ds


def load_tinyimagenet_dataset(num_examples, seed):
    data_dir = "tinyimagenet/tiny-imagenet-200/train"
    tiny_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        shuffle=False,
        image_size=(32, 32),
        batch_size=None)

    norm_layer = tf.keras.layers.Normalization(mean=[0.4914, 0.4822, 0.4465],
                                               variance=[np.square(0.2023),
                                                         np.square(0.1994),
                                                         np.square(0.2010)])

    tiny_ds = tiny_ds.shuffle(60000, seed=seed, reshuffle_each_iteration=False)
    tiny_ds = tiny_ds.take(num_examples)
    tiny_ds = tiny_ds.map(
        lambda x, y: (norm_layer(tf.cast(x, tf.float32) / 255.0),
                         y))

    return tiny_ds


def load_transfer_set(dataset_name, num_examples, seed):
    if dataset_name == "svhn":
        if num_examples == -1:
            n = 73257 + 26032
            return load_svhn_dataset(n, seed=seed)
        return load_svhn_dataset(num_examples, seed=seed)
    elif dataset_name == "sop":
        if num_examples == -1:
            n = 60502 + 59551
            load_stanford_online_products_dataset(n, seed=seed)
        return load_stanford_online_products_dataset(num_examples, seed=seed)
    elif dataset_name == "stl10":
        if num_examples == -1:
            n = 100000
            return load_stl10_dataset(n, seed=seed)
        return load_stl10_dataset(num_examples, seed=seed)
    elif dataset_name == "cifar100":
        if num_examples == -1:
            n = 60000
            return load_cifar100_dataset(n, seed=seed)
        return load_cifar100_dataset(num_examples, seed=seed)
    elif dataset_name == "random":
        return load_random_dataset(num_examples, seed=seed)
    elif dataset_name == "dtd":
        if num_examples == -1:
            n = 1880*3
            return load_dtd_dataset(n, seed=seed)
        return load_dtd_dataset(1880*3, seed=seed)
    elif dataset_name == "tiny":
        if num_examples == -1:
            n = 100000
            return load_tinyimagenet_dataset(n, seed=seed)
        return load_tinyimagenet_dataset(num_examples, seed=seed)
    else:
        # loading cifar10 dataset
        if num_examples == -1:
            n = 60000
            return load_cifar10_dataset(n, seed=seed)
        return load_cifar10_dataset(num_examples, seed=seed)
