<template>
    <canvas id="canvas"></canvas>
    <div id="spinner"></div>
    <div id="fps"></div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        cameras: [],
        camera: null,
        worker: null,
        gl: null,
        viewMatrix: [],
        projectionMatrix: [],
        vertexCount: 0,
        modelURL: "./model.splatv", // 需要加载的 `.splatv` 文件
      };
    },
    async mounted() {
      await this.initialize();
    },
    methods: {
      async initialize() {
        const canvas = document.getElementById("canvas");
        this.gl = canvas.getContext("webgl2", { antialias: false });
  
        this.setupShaders();
        this.setupWorker();
        await this.loadSplatvFile(this.modelURL); // 加载 `.splatv` 文件
        this.startRendering();
      },
      
      setupShaders() {
        const gl = this.gl;
        const vertexShaderSource = `...`; // 你的 vertex shader 代码
        const fragmentShaderSource = `...`; // 你的 fragment shader 代码
  
        const vertexShader = gl.createShader(gl.VERTEX_SHADER);
        gl.shaderSource(vertexShader, vertexShaderSource);
        gl.compileShader(vertexShader);
  
        const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(fragmentShader, fragmentShaderSource);
        gl.compileShader(fragmentShader);
  
        const program = gl.createProgram();
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);
        gl.useProgram(program);
  
        gl.disable(gl.DEPTH_TEST);
        gl.enable(gl.BLEND);
        gl.blendFuncSeparate(gl.ONE_MINUS_DST_ALPHA, gl.ONE, gl.ONE_MINUS_DST_ALPHA, gl.ONE);
      },
  
      setupWorker() {
        const workerCode = `
          self.onmessage = (e) => {
            if (e.data.splatData) {
              const data = e.data.splatData;
              console.log("Worker processing .splatv file with size:", data.byteLength);
              self.postMessage({ result: "Processed", vertexCount: data.byteLength / 16 });
            }
          };
        `;
  
        const blob = new Blob([workerCode], { type: "application/javascript" });
        this.worker = new Worker(URL.createObjectURL(blob));
  
        this.worker.onmessage = (e) => {
          console.log("Main thread received:", e.data);
          this.vertexCount = e.data.vertexCount;
        };
      },
  
      async loadSplatvFile(url) {
        try {
          const response = await fetch(url, { mode: "cors", credentials: "omit" });
          if (!response.ok) throw new Error(`Failed to load .splatv: ${response.status}`);
  
          const arrayBuffer = await response.arrayBuffer();
          console.log("Loaded .splatv file, size:", arrayBuffer.byteLength);
  
          this.worker.postMessage({ splatData: arrayBuffer }, [arrayBuffer]);
        } catch (error) {
          console.error("Error loading .splatv file:", error);
        }
      },
  
      startRendering() {
        const render = () => {
          if (this.vertexCount > 0) {
            this.renderScene();
          }
          requestAnimationFrame(render);
        };
        render();
      },
  
      renderScene() {
        const gl = this.gl;
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
      },
    },
  };
  </script>
  
  <style scoped>
  canvas {
    width: 100vw;
    height: 100vh;
    display: block;
  }
  </style>
  