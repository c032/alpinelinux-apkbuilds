package main

import (
	"flag"
	"fmt"
	"io/fs"
	"log/slog"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	log := slog.Default()

	flag.Parse()

	args := flag.Args()
	if len(args) != 1 {
		panic("expected exactly one arg")
	}

	vendorDirectory := args[0]

	err := filepath.Walk(vendorDirectory, func(path string, fi fs.FileInfo, err error) error {
		if err != nil {
			return err
		}

		name := fi.Name()
		if !strings.Contains(name, "@") {
			return nil
		}

		parts := strings.SplitN(name, "@", 2)
		newName := parts[0]

		dirName := filepath.Dir(path)
		newPath := filepath.Join(dirName, newName)

		log.Info(
			"Renaming.",
			"from", path,
			"to", newPath,
		)
		err = os.Rename(path, newPath)
		if err != nil {
			return fmt.Errorf("failed to rename from %#v to %#v: %w", path, newPath, err)
		}

		return filepath.SkipDir
	})
	if err != nil {
		panic(err)
	}
}
