import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def modaddplot(df):
    preproc = pd.DataFrame({
        'Bits': list(df[df.method == 'ModAddBig'].bits),
        'Big': list(df[df.method == 'ModAddBig'].ns),
        'Nat': list(df[df.method == 'ModAddNat'].ns),
    })
    ax = preproc.plot(x="Bits", y="Nat", legend=False)
    ax2 = ax.twinx()
    preproc.plot(x="Bits", y="Big", ax=ax2, legend=False, color="r")
    ax.figure.legend()
    plt.title('ModAdd Execution Time')
    plt.savefig('./.out/modadd.png')
    pass

def expplot(df):
    preproc = pd.DataFrame({
        'Hamming Weight': list(df[df.method == 'ModExpBig'].bits),
        'Big': list(df[df.method == 'ModExpBig'].ns),
        'Nat': list(df[df.method == 'ModExpNat'].ns),
    })
    ax = preproc.plot(x="Hamming Weight", y="Nat", legend=False)
    ax2 = ax.twinx()
    preproc.plot(x="Hamming Weight", y="Big", ax=ax2, legend=False, color="r")
    ax.figure.legend()
    plt.title('Exp Execution Time')
    plt.savefig('./.out/exp.png')


def main():
    df = pd.read_csv("./.out/samples.csv")
    modaddplot(df)
    expplot(df)


if __name__ == "__main__":
    main()
