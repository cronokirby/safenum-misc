import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def modaddplot(df):
    preproc = pd.DataFrame(
        {
            "Bits": list(df[df.method == "ModAddBig"].bits),
            "Big": list(df[df.method == "ModAddBig"].ns),
            "Nat": list(df[df.method == "ModAddNat"].ns),
        }
    )
    ax = plt.subplot(2, 1, 1)
    preproc.plot(x="Bits", y="Nat", ax=ax, legend=False, xlabel="", ylabel="ns")
    plt.title("ModAdd Execution Time (Nat)")
    ax = plt.subplot(2, 1, 2)
    preproc.plot(x="Bits", y="Big", ax=ax, legend=False, color="r", ylabel="ns")
    plt.title("ModAdd Execution Time (Big)")
    plt.tight_layout()
    plt.savefig("./.out/modadd.png")
    pass


def expplot(df):
    preproc = pd.DataFrame(
        {
            "Hamming Weight": list(df[df.method == "ModExpBig"].bits),
            "Big": list(df[df.method == "ModExpBig"].ns),
            "Nat": list(df[df.method == "ModExpNat"].ns),
        }
    )
    plt.clf()
    ax = plt.subplot(2, 1, 1)
    preproc.plot(
        x="Hamming Weight", y="Nat", ax=ax, legend=False, xlabel="", ylabel="ns"
    )
    plt.title("Exp Execution Time (Nat)")
    ax = plt.subplot(2, 1, 2)
    preproc.plot(
        x="Hamming Weight", y="Big", ax=ax, legend=False, color="r", ylabel="ns"
    )
    plt.title("Exp Execution Time (Big)")
    plt.savefig("./.out/exp.png")


def main():
    df = pd.read_csv("./.out/samples.csv")
    modaddplot(df)
    expplot(df)


if __name__ == "__main__":
    main()
