package main

import (
	"crypto/rand"
	"encoding/csv"
	"fmt"
	"log"
	"math/big"
	"os"
	"time"

	"github.com/cronokirby/safenum"
)

func natSized(bits int) *safenum.Nat {
	// This makes sure that our thing is smaller than the modulus
	data := make([]byte, (bits+7)/8)
	_, _ = rand.Read(data)
	return new(safenum.Nat).SetBytes(data).Resize(bits)
}

func mod2048() *safenum.Modulus {
	data := make([]byte, 2048/8)
	for i := 0; i < len(data); i++ {
		data[i] = 0xFF
	}
	return safenum.ModulusFromBytes(data)
}

func bigSized(bits int) *big.Int {
	return natSized(bits).Big()
}

func modBig() *big.Int {
	return mod2048().Big()
}

func timeFunction(f func()) time.Duration {
	start := time.Now()
	f()
	return time.Since(start)
}

const maxBits = 4096

var resultBig *big.Int
var resultNat *safenum.Nat

func modAddBigSamples(w *csv.Writer) error {
	m := modBig()
	for i := 0; i < maxBits; i++ {
		x := bigSized(i)
		t := timeFunction(func() {
			x.Add(x, x)
			resultBig = x.Mod(x, m)
		})
		if err := w.Write([]string{"ModAddBig", fmt.Sprintf("%d", i), fmt.Sprintf("%d", t)}); err != nil {
			return err
		}
	}
	w.Flush()
	return w.Error()
}

func modAddNatSamples(w *csv.Writer) error {
	m := mod2048()
	for i := 0; i < maxBits; i++ {
		x := natSized(i).Resize(maxBits)
		t := timeFunction(func() {
			resultNat = x.ModAdd(x, x, m)
		})
		if err := w.Write([]string{"ModAddNat", fmt.Sprintf("%d", i), fmt.Sprintf("%d", t)}); err != nil {
			return err
		}
	}
	w.Flush()
	return w.Error()
}

func csvA() error {
	w := csv.NewWriter(os.Stdout)
	if err := w.Write([]string{"method", "bits", "ns"}); err != nil {
		return err
	}
	if err := modAddBigSamples(w); err != nil {
		return err
	}
	if err := modAddNatSamples(w); err != nil {
		return err
	}
	w.Flush()
	return w.Error()
}

func main() {
	if err := csvA(); err != nil {
		log.Fatal(err)
	}
}
