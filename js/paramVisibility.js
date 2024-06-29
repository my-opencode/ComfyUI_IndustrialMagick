//@ts-check
// import { app } from "../../../web/scripts/app.js";
import { app } from "../../scripts/app.js";

let origProps = {};
let initialized = false;
const HIDDEN_TAG = "tschide";

function handleParamVisibility(node, countValue) {
    for (let i = 1; i <= 50; i++) {
        const pname = `param_${i}`;
        const paramWidget = node.widgets.find((w) => w.name === pname);
        if (!paramWidget) continue;

        if (!origProps[pname]) {
            origProps[pname] = { origType: paramWidget.type, origComputeSize: paramWidget.computeSize };
        }

        if (i <= countValue || node.inputs?.some?.(input => input.name === pname)) {
            paramWidget.type = origProps[pname].origType;
            paramWidget.computeSize = origProps[pname].origComputeSize;
        }
        else {
            paramWidget.type = HIDDEN_TAG;
            paramWidget.computeSize = () => [0, -4];
        }
    }
    const newHeight = node.computeSize()[1];
    node.setSize([node.size[0], newHeight]);
}

function registerIndustrialMagickParamVisibility(node) {
    for (const w of node.widgets || []) {
        if (w.name !== "param_count") continue;
        let countValue = w.value;
        // Store the original descriptor if it exists
        let originalDescriptor = Object.getOwnPropertyDescriptor(w, 'value');
        handleParamVisibility(node, countValue);
        Object.defineProperty(w, 'value', {
            get() {
                // If there's an original getter, use it. Otherwise, return widgetValue.
                let valueToReturn = originalDescriptor && originalDescriptor.get
                    ? originalDescriptor.get.call(w)
                    : countValue;

                return valueToReturn;
            },
            set(newVal) {
                // If there's an original setter, use it. Otherwise, set widgetValue.
                if (originalDescriptor && originalDescriptor.set) {
                    originalDescriptor.set.call(w, newVal);
                } else {
                    countValue = newVal;
                }
                handleParamVisibility(node, countValue);
            }
        });
    }
}

app.registerExtension({
    name: "industrialmagick.paramvisibility",
    nodeCreated(node) {
        if (node.comfyClass === "IndustrialMagick")
            registerIndustrialMagickParamVisibility(node);
        setTimeout(() => { initialized = true; }, 500);
    }
});

