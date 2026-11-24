"""
Replicates the Colab sed patch for mediafire/subsetio.py:
  sed -i 's/self.parent_fd.fileno()/try:\\n...except (ValueError, OSError):\\n    pass/'
Using Python so multiline replacement is reliable across platforms.
"""
import os
import site
import sys


def find_subsetio():
    for base in site.getsitepackages():
        candidate = os.path.join(base, "mediafire", "subsetio.py")
        if os.path.exists(candidate):
            return candidate
    # fallback: ask Python where mediafire lives
    try:
        import mediafire
        candidate = os.path.join(os.path.dirname(mediafire.__file__), "subsetio.py")
        if os.path.exists(candidate):
            return candidate
    except ImportError:
        pass
    return None


def main():
    target = find_subsetio()
    if not target:
        print("WARNING: mediafire/subsetio.py not found – skipping patch", file=sys.stderr)
        return

    with open(target) as f:
        src = f.read()

    old = "self.parent_fd.fileno()"
    new = (
        "try:\n"
        "                self.parent_fd.fileno()\n"
        "            except (ValueError, OSError):\n"
        "                pass"
    )

    patched = src.replace(old, new)
    if patched == src:
        print(f"Pattern not found in {target} – already patched or mismatch, skipping")
        return

    with open(target, "w") as f:
        f.write(patched)
    print(f"✓ Patched {target}")


if __name__ == "__main__":
    main()
