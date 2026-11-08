import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js';

export interface SceneConfig {
  canvas: HTMLCanvasElement;
  dracoPath: string;
  basisTranscoderPath: string;
}

export class ProductionWebGPUScene {
  private renderer!: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private animationFrameId: number | null = null;
  private gltfLoader: GLTFLoader;

  constructor(config: SceneConfig) {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera.position.set(0, 2, 5);

    // Initialize renderer with clamped DPR and sRGB ACESFilmic tone mapping
    this.renderer = new THREE.WebGLRenderer({
      canvas: config.canvas,
      antialias: true,
      powerPreference: 'high-performance',
    });
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.0;
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0));
    this.renderer.setSize(window.innerWidth, window.innerHeight);

    // Setup asset loaders with worker decoders
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath(config.dracoPath);

    const ktx2Loader = new KTX2Loader();
    ktx2Loader.setTranscoderPath(config.basisTranscoderPath);
    ktx2Loader.detectSupport(this.renderer);

    this.gltfLoader = new GLTFLoader();
    this.gltfLoader.setDRACOLoader(dracoLoader);
    this.gltfLoader.setKTX2Loader(ktx2Loader);

    // Setup WebGL Context Loss Handlers
    config.canvas.addEventListener('webglcontextlost', this.onContextLost, false);
    config.canvas.addEventListener('webglcontextrestored', this.onContextRestored, false);

    window.addEventListener('resize', this.onResize);
  }

  private onContextLost = (e: Event) => {
    e.preventDefault();
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  };

  private onContextRestored = () => {
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.startRenderLoop();
  };

  private onResize = () => {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  };

  public async loadAsset(url: string): Promise<THREE.Group> {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        url,
        (gltf) => {
          this.scene.add(gltf.scene);
          resolve(gltf.scene);
        },
        undefined,
        (error) => reject(error)
      );
    });
  }

  public startRenderLoop() {
    const render = () => {
      this.renderer.render(this.scene, this.camera);
      this.animationFrameId = requestAnimationFrame(render);
    };
    render();
  }

  public dispose() {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
    }
    window.removeEventListener('resize', this.onResize);

    // Deep GPU disposal
    this.scene.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        object.geometry?.dispose();
        if (Array.isArray(object.material)) {
          object.material.forEach((m) => m.dispose());
        } else {
          object.material?.dispose();
        }
      }
    });

    this.renderer.dispose();
  }
}
