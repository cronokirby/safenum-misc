import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def modaddplot(df):
    preproc = pd.DataFrame(
        {
            "Bits": list(df[df.method == "ModAddBig"].bits),
            "Go's big.Int": list(df[df.method == "ModAddBig"].ns),
            "safenum": list(df[df.method == "ModAddNat"].ns),
        }
    )
    plt.clf()
    ax = plt.subplot(1, 1, 1)
    preproc.plot(x="Bits", y="Go's big.Int", ax=ax, legend=False, color="r", ylabel="ns")
    preproc.plot(x="Bits", y="safenum", ax=ax, legend=False, xlabel="", ylabel="ns")
    ax.figure.legend()
    plt.title("Execution time of Modular Addition")
    fig = plt.gcf()
    fig.set_size_inches(7.5, 4)
    plt.tight_layout()
    plt.savefig("./.out/modadd.png")
    pass


def expplot(df):
    preproc = pd.DataFrame(
        {
            "Hamming Weight": list(df[df.method == "ModExpBig"].bits),
            "Go's big.Int": list(df[df.method == "ModExpBig"].ns),
            "safenum": list(df[df.method == "ModExpNat"].ns),
        }
    )
    plt.clf()
    ax = plt.subplot(1, 1, 1)
    preproc.plot(
        x="Hamming Weight", y="Go's big.Int", ax=ax, legend=False, color="r", ylabel="ns",
        logy=False
    )
    preproc.plot(
        x="Hamming Weight", y="safenum", ax=ax, legend=False, xlabel="", ylabel="ns",
        logy=False
    )
    ax.figure.legend()
    plt.title("Execution time of Exponentiation")
    fig = plt.gcf()
    fig.set_size_inches(7.5, 4)
    plt.tight_layout()
    plt.savefig("./.out/exp.png")


def main():
    df = pd.read_csv("./.out/samples.csv")
    modaddplot(df)
    expplot(df)


if __name__ == "__main__":
    main()
