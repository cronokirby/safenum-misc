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

func withHammingWeight(maxBits int, h int) *safenum.Nat {
	hi := new(safenum.Nat).SetUint64(1).Resize(1)
	hi.Lsh(hi, uint(maxBits)-1, -1)
	lo := new(safenum.Nat).SetUint64(1).Resize(1)
	lo.Lsh(lo, uint(h), -1)
	lo.Sub(lo, new(safenum.Nat).SetUint64(1), -1)
	return hi.Add(hi, lo, maxBits)
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

const average = 400

func timeFunction(f func()) time.Duration {

	start := time.Now()

	for i := 0; i < average; i++ {
		f()
	}
	return time.Since(start) / average
}

const maxBits = 4096
const expBits = 64

var resultBig *big.Int = new(big.Int)
var resultNat *safenum.Nat = new(safenum.Nat)

func modAddBigSamples(w *csv.Writer) error {
	m := modBig()
	for i := 0; i < maxBits; i++ {
		x := bigSized(i)
		t := timeFunction(func() {
			resultBig.Add(x, x)
			resultBig.Mod(resultBig, m)
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
		resultNat.Resize(maxBits)
		t := timeFunction(func() {
			resultNat.ModAdd(x, x, m)
		})
		if err := w.Write([]string{"ModAddNat", fmt.Sprintf("%d", i), fmt.Sprintf("%d", t)}); err != nil {
			return err
		}
	}
	w.Flush()
	return w.Error()
}

func expBigSamples(w *csv.Writer) error {
	m := modBig()
	x := bigSized(m.BitLen())
	x.Mod(x, m)
	for i := 0; i < expBits; i++ {
		y := withHammingWeight(expBits, i).Big()
		t := timeFunction(func() {
			resultBig.Exp(x, y, m)
		})
		if err := w.Write([]string{"ModExpBig", fmt.Sprintf("%d", i+1), fmt.Sprintf("%d", t)}); err != nil {
			return err
		}
	}
	w.Flush()
	return w.Error()
}

func expNatSamples(w *csv.Writer) error {
	m := mod2048()
	x := natSized(m.BitLen())
	x.Mod(x, m)
	for i := 0; i < expBits; i++ {
		y := withHammingWeight(expBits, i)
		t := timeFunction(func() {
			resultNat.Exp(x, y, m)
		})
		if err := w.Write([]string{"ModExpNat", fmt.Sprintf("%d", i+1), fmt.Sprintf("%d", t)}); err != nil {
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
	if err := expBigSamples(w); err != nil {
		return err
	}
	if err := expNatSamples(w); err != nil {
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
