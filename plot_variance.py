import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def modaddplot(df):
    preproc = pd.DataFrame(
        {
            "Bits": list(df[df.method == "ModAddBig"].bits),
            "Go's big.Int": list(df[df.method == "ModAddBig"].ns / 1000),
            "saferith": list(df[df.method == "ModAddNat"].ns / 1000),
        }
    )
    plt.clf()
    ax = plt.subplot(1, 1, 1)
    preproc.plot(x="Bits", y="Go's big.Int", ax=ax, legend=False, color="r", ylabel="μs")
    preproc.plot(x="Bits", y="saferith", ax=ax, legend=False, xlabel="", ylabel="μs")
    plt.xlabel('Significant Bits')
    plt.xticks(np.arange(0, 4 * 1024 + 1, 1024))
    ax.figure.legend(bbox_to_anchor=(1.0, 1.06), loc="upper right")
    plt.title("Execution time of Modular Addition with 2048 bit modulus", loc="left")
    fig = plt.gcf()
    fig.set_size_inches(8.1, 4)
    plt.tight_layout()
    plt.savefig("./.out/modadd.png", bbox_inches="tight")
    pass


def expplot(df):
    preproc = pd.DataFrame(
        {
            "Hamming Weight": list(df[df.method == "ModExpBig"].bits),
            "Go's big.Int": list(df[df.method == "ModExpBig"].ns / 1000),
            "saferith": list(df[df.method == "ModExpNat"].ns / 1000),
        }
    )
    plt.clf()
    ax = plt.subplot(1, 1, 1)
    preproc.plot(
        x="Hamming Weight", y="Go's big.Int", ax=ax, legend=False, color="r", ylabel="μs",
        logy=False
    )
    preproc.plot(
        x="Hamming Weight", y="saferith", ax=ax, legend=False, xlabel="", ylabel="μs",
        logy=False
    )
    plt.xlabel('Number of 1 bits in exponent')
    plt.xticks(np.arange(0, 64 + 1, 16))
    ax.figure.legend(bbox_to_anchor=(1.0, 1.06), loc="upper right")
    plt.title("Execution time of Exponentiation with 64 bit exponent, 2048 bit base", loc='left')
    fig = plt.gcf()
    fig.set_size_inches(8.1, 4)
    plt.tight_layout()
    plt.savefig("./.out/exp.png", bbox_inches="tight")


def main():
    df = pd.read_csv("./.out/samples.csv")
    modaddplot(df)
    expplot(df)


if __name__ == "__main__":
    main()
