from flask import Flask, render_template, request, abort
from topology_engine import TopologyEngine

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error  = None

    if request.method == "POST":
        try:
            nodes  = int(request.form.get("nodes", 0))
            prefix = request.form.get("prefix", "").strip().upper()

            if nodes <= 0:
                raise ValueError("Device count must be greater than zero.")
            if not prefix:
                raise ValueError("VLAN name prefix cannot be empty.")

            engine = TopologyEngine()
            topo   = engine.design(nodes, prefix)

            result = {
                "switches": len(topo.switches),
                "vlans":    len(topo.segments),
                "uplinks":  len(topo.uplinks),
                "segments": topo.segments,
            }

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Design failed: {str(e)}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)