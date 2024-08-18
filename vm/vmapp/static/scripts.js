const memoryData = document.getElementById("memory-data");
const registersData = document.getElementById("registers-data");
const programCounter = document.getElementById("program-counter");
const instructionRegister = document.getElementById("instruction-register");
const opcode = document.getElementById("opcode");
const operands = document.getElementById("operands");
const assemblyCode = document.getElementById("assembly-code");
const machineCode = document.getElementById("machine-code");
const displayCanvas = document.getElementById("display-canvas");
const canvasContainer = document.getElementById("canvas-container");
const ctx = displayCanvas.getContext("2d");
let displayOn = true;
let startTime;
let stepDelay = 500; // Default to 500ms per step

function updateUI(data) {
  loadMemory(data.memory);
  loadRegisters(data.registers);
  programCounter.value = data.program_counter
    .toString(16)
    .padStart(2, "0")
    .toUpperCase();
  instructionRegister.value = data.instruction_register
    .toString(16)
    .padStart(4, "0")
    .toUpperCase();
  opcode.value = data.opcode.toString(16).toUpperCase();
  operands.value = `${data.operands[0]}, ${data.operands[1]}, ${data.operands[2]}`;
  if (data.halted) {
    const endTime = performance.now();
    const runningTime = (endTime - startTime) / 1000;
    alert(
      `The virtual machine has halted. Running time: ${runningTime.toFixed(
        2
      )} seconds.`
    );
  }
  if (displayOn) {
    updateDisplay(data.memory);
  }
}

function loadMemory(memory) {
  memoryData.innerHTML = "";
  memory.forEach((item, index) => {
    const row = document.createElement("tr");

    const binaryValue = item.toString(2).padStart(8, "0");
    const hexValue = item.toString(16).padStart(2, "0").toUpperCase();
    const integerValue = item.toString(10);
    const floatValue = parseFloat(item).toFixed(3);

    row.innerHTML = `
            <td>${index.toString(16).padStart(2, "0").toUpperCase()}</td>
            <td>
                <input type="text" class="narrow-input" value="${binaryValue}" onchange="syncMemoryFields(${index}, this.value, 'binary')">
            </td>
            <td>
                <input type="text" class="narrow-input" value="${hexValue}" onchange="syncMemoryFields(${index}, this.value, 'hex')">
            </td>
            <td>
                <input type="text" class="narrow-input" value="${integerValue}" onchange="syncMemoryFields(${index}, this.value, 'integer')">
            </td>
            <td>
                <input type="text" class="narrow-input" value="${floatValue}" onchange="syncMemoryFields(${index}, this.value, 'float')">
            </td>
            <td></td>
        `;
    memoryData.appendChild(row);
  });
}

function loadRegisters(registers) {
  registersData.innerHTML = "";
  registers.forEach((item, index) => {
    const row = document.createElement("tr");

    const binaryValue = item.toString(2).padStart(8, "0");
    const integerValue = item.toString(10);

    row.innerHTML = `
            <td>${index.toString(16).toUpperCase()}</td>
            <td>
                <input type="text" class="narrow-input" value="${binaryValue}" onchange="syncRegisterFields(${index}, this.value, 'binary')">
            </td>
            <td>${item.toString(16).padStart(2, "0").toUpperCase()}</td>
            <td>
                <input type="text" class="narrow-input" value="${integerValue}" onchange="syncRegisterFields(${index}, this.value, 'integer')">
            </td>
            <td>${parseFloat(item).toFixed(3)}</td>
        `;
    registersData.appendChild(row);
  });
}

function syncMemoryFields(index, value, type) {
  let newValue;

  switch (type) {
    case "binary":
      newValue = parseInt(value, 2);
      break;
    case "hex":
      newValue = parseInt(value, 16);
      break;
    case "integer":
      newValue = parseInt(value, 10);
      break;
    case "float":
      newValue = parseFloat(value);
      break;
    default:
      break;
  }

  if (!isNaN(newValue)) {
    // Update the memory in the backend
    fetch("/api/vmonline4/update_memory/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ index: index, value: newValue }),
    })
      .then((response) => response.json())
      .then((data) => updateUI(data))
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while updating the memory.");
      });
  } else {
    alert("Invalid value");
  }
}

function syncRegisterFields(index, value, type) {
  let newValue;
  if (type === "binary") {
    newValue = parseInt(value, 2);
  } else if (type === "integer") {
    newValue = parseInt(value, 10);
  }

  if (!isNaN(newValue)) {
    // Update the registers in the backend
    fetch("/api/vmonline4/update_register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ index: index, value: newValue }),
    })
      .then((response) => response.json())
      .then((data) => updateUI(data))
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while updating the register.");
      });
  } else {
    alert("Invalid value");
  }
}

function loadMachineCode() {
  const link= document.createElement("a");
  link.download = ".txt";
  link.href = displayCanvas.toDataURL("txt");
  link.click();
}

function resetVM() {
  fetch("/api/vmonline4/reset/")
    .then((response) => response.json())
    .then((data) => {
      updateUI(data);
      alert("Virtual machine reset successfully.");
    });
}

function doStep() {
  fetch("/api/vmonline4/step/")
    .then((response) => response.json())
    .then((data) => updateUI(data));
}

async function runVM() {
  startTime = performance.now();
  while (true) {
    const response = await fetch("/api/vmonline4/step/");
    const data = await response.json();
    updateUI(data);
    if (data.halted) break;
    await new Promise((resolve) => setTimeout(resolve, stepDelay));
  }
}

function updateSpeed() {
  const speedRange = document.getElementById("speed");
  const speedValue = parseInt(speedRange.value, 10);
  stepDelay = (100 - speedValue) * 10; // 0ms to 1000ms delay
}

function displayAssemblyCode(code) {
  assemblyCode.textContent = code;
}

function displayMachineCode(code) {
  machineCode.textContent = code;
}

function stripComments(code) {
  return code
    .split("\n")
    .map((line) => line.split(";")[0].trim())
    .filter((line) => line.length > 0)
    .join("\n");
}

function editMemory(index, value) {
  const newValue = parseInt(value, 16);
  if (!isNaN(newValue)) {
    fetch("/api/vmonline4/update_memory/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ index: index, value: newValue }),
    })
      .then((response) => response.json())
      .then((data) => updateUI(data))
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while updating the memory.");
      });
  } else {
    alert("Invalid hex value");
  }
}

function updateDisplay(memory) {
  const displaySize = 32;
  const scale = 20; // Scale each bit to 20x20 pixels
  ctx.clearRect(0, 0, displayCanvas.width, displayCanvas.height);

  for (let row = 0; row < displaySize; row++) {
    for (let col = 0; col < displaySize; col++) {
      const byteIndex = 0x80 + Math.floor((row * displaySize + col) / 8);
      const bitIndex = 7 - (col % 8);
      const byte = memory[byteIndex];
      const color = byte & (1 << bitIndex) ? 255 : 0;

      ctx.fillStyle = `rgb(${color}, ${color}, ${color})`;
      ctx.fillRect(col * scale, row * scale, scale, scale);
    }
  }
}

function toggleDisplay() {
  displayOn = !displayOn;
  if (displayOn) {
    // alert("Display turned on.");
    canvasContainer.style.visibility = "visible";
  } else {
    // alert("Display turned off.");
    canvasContainer.style.visibility = "hidden";
  }
}

function saveDisplay() {
  const link = document.createElement("a");
  link.download = "display.png";
  link.href = displayCanvas.toDataURL("image/png");
  link.click();
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document
  .getElementById("input-file")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
      const content = e.target.result;
      const strippedContent = stripComments(content);
      displayAssemblyCode(strippedContent);
    };
    reader.readAsText(file);
  });

document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData();
    const inputFile = document.getElementById("input-file").files[0];
    formData.append("input_file", inputFile);

    const csrftoken = getCookie("csrftoken");
    fetch("/api/upload_file/", {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "assembled") {
          console.log("Machine code:", data.machine_code);
          displayMachineCode(data.machine_code);
          alert("File uploaded and assembled successfully!");
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while uploading the file.");
      });
  });

var instructionsModal = document.getElementById("instructions");
var instructionsBtn = document.getElementById("openInstructionsBtn");
var instructionsSpan = document.getElementsByClassName("instructions-close")[0];

instructionsBtn.onclick = function () {
  instructionsModal.style.display = "block";
};
instructionsSpan.onclick = function () {
  instructionsModal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == instructionsModal) {
    instructionsModal.style.display = "none";
  }
};

var helpModal = document.getElementById("help");
var helpBtn = document.getElementById("openHelpBtn");
var helpSpan = document.getElementsByClassName("help-close")[0];

helpBtn.onclick = function () {
  helpModal.style.display = "block";
};
helpSpan.onclick = function () {
  helpModal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == helpModal) {
    helpModal.style.display = "none";
  }
};

var assemblerHelpModal = document.getElementById("assembler-help");
var assemblerHelpBtn = document.getElementById("openAssemblerHelpBtn");
var assemblerHelpSpan = document.getElementsByClassName(
  "assembler-help-close"
)[0];

assemblerHelpBtn.onclick = function () {
  assemblerHelpModal.style.display = "block";
};
assemblerHelpSpan.onclick = function () {
  assemblerHelpModal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == assemblerHelpModal) {
    assemblerHelpModal.style.display = "none";
  }
};

window.onload = resetVM;
