"""show(plot, name): window if interactive, PNG if run with --save DIR."""
import sys, os
def show(p, name):
    if "--save" in sys.argv:
        i = sys.argv.index("--save"); out = sys.argv[i+1] if len(sys.argv) > i+1 else "."
        os.makedirs(out, exist_ok=True); p.save(os.path.join(out, name), dpi=120, verbose=False)
        print("saved", os.path.join(out, name))
    else:
        p.show()
