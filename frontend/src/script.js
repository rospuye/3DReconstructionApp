import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'



/**
 * Base
 */

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()
scene.background = new THREE.Color(0xffffff);

/*0
 * Models
 */
const dracoLoader = new DRACOLoader()
dracoLoader.setDecoderPath('/draco/')

const gltfLoader = new GLTFLoader()
gltfLoader.setDRACOLoader(dracoLoader)

let mixer = null

const ANGLE = Math.PI /36; // 9;
var model;

gltfLoader.load(
    '/models/Duck/glTF/Duck.gltf',
    (gltf) => {
        gltf.scene.scale.set(3,3,3)
        // gltf.scene.position.set(0,0,0)
        model = gltf.scene;
        scene.add(model)
        gltf.scene.rotation.y = 0 * ANGLE;



        gltf.scene.rotation.x = 71 * ANGLE;
    }
)

/**
 * Lights
 */
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8)
scene.add(ambientLight)

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6)
directionalLight.castShadow = true
directionalLight.shadow.mapSize.set(1024, 1024)
directionalLight.shadow.camera.far = 15
directionalLight.shadow.camera.left = - 7
directionalLight.shadow.camera.top = 7
directionalLight.shadow.camera.right = 7
directionalLight.shadow.camera.bottom = - 7
directionalLight.position.set(- 5, 5, 0)
scene.add(directionalLight)

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () => {
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
// camera.position.set(2,2,2) // for duck
camera.position.set(0, -1, -3)
scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.target.set(0, 0.75, 0)
controls.enableDamping = true

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Capture of model 
 */

// function debugBase64(base64URL){
//     var win = window.open();
//     win.document.write('<iframe src="' + base64URL  + '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;" allowfullscreen></iframe>');
// }

// function delay(time) {
//     return new Promise(resolve => setTimeout(resolve, time));
// }

// document.onkeypress = function (e) {
//     e = e || window.event;
//     if (e.keyCode == 32) {

//         // console.log('hi');

//         for (let i=0; i<4; i++) {
//             // console.log(i)
//             setTimeout(() => { model.rotation.y = i * ANGLE; }, 1000);
//         } 


//         // const screenshotTarget = document.body;
//         // html2canvas(screenshotTarget).then((canvas) => {
//         //     const base64image = canvas.toDataURL("image/png");
//         //     // window.location.href = base64image;
//         //     debugBase64(base64image)
//         // });
//     }
// };

/**
 * Animate
 */
const clock = new THREE.Clock()
let previousTime = 0

const tick = () => {
    const elapsedTime = clock.getElapsedTime()
    const deltaTime = elapsedTime - previousTime
    previousTime = elapsedTime

    // if (model) {
    //     if (model.rotation.y % ANGLE == 0) {
    //         console.log('ha!')
    //     } 
    //     model.rotation.y += ANGLE;
    //     model.rotation.y = model.rotation.y % (2*Math.PI)
    // }

    // Update controls
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()