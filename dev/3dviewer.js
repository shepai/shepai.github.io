

for(let i=0; i<stlFiles.length; i++){

    createSTLViewer(
        containers[i],
        stlFiles[i]
    );

}

function createSTLViewer(containerID, url){


    let container = document.getElementById(containerID);

	let mesh = null;
    // Scene
    let scene = new THREE.Scene();



    // Camera
    let camera = new THREE.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );


    camera.position.set(
        0,
        0,
        100
    );



    // Renderer
    let renderer = new THREE.WebGLRenderer({
        antialias:true,
        alpha:true
    });


    renderer.setSize(
        container.clientWidth,
        container.clientHeight
    );


    container.innerHTML = "";
    container.appendChild(
        renderer.domElement
    );



    // Lighting

    let light = new THREE.DirectionalLight(
        0xffffff,
        2
    );


    light.position.set(
        1,
        1,
        1
    );


    scene.add(light);


    scene.add(
        new THREE.AmbientLight(
            0xffffff,
            0.8
        )
    );



    // Loading text

    let loadingText = document.createElement("p");

    loadingText.innerHTML = "Loading STL...";

    container.appendChild(
        loadingText
    );



    // STL loader

    let loader = new THREE.STLLoader();



    loader.load(

        url,


        function(geometry){


            console.log(
                "Loaded:",
                url
            );


            loadingText.remove();



            geometry.computeBoundingBox();

            geometry.center();



            let material = new THREE.MeshPhongMaterial({

                color:0x888888

            });



            mesh = new THREE.Mesh(
				geometry,
				material
			);


            scene.add(mesh);
			mesh.rotation.x = -Math.PI / 4;
			mesh.rotation.z = Math.PI / 6;


            // Scale model

            let size = geometry.boundingBox.getSize(

                new THREE.Vector3()

            );


            let maxDim = Math.max(

                size.x,

                size.y,

                size.z

            );


            let scale = 30 / maxDim;

mesh.scale.setScalar(scale);


// move camera automatically
camera.position.set(
    0,
    0,
    100
);

camera.lookAt(
    0,
    0,
    0
);



        },



        function(xhr){


            if(xhr.total > 0){

                let percent = (

                    xhr.loaded / xhr.total * 100

                ).toFixed(0);



                loadingText.innerHTML =

                    "Loading STL: " + percent + "%";

            }


        },



        function(error){


            console.error(

                "Failed loading:",

                url,

                error

            );


            loadingText.innerHTML =
                "Failed to load STL";


        }


    );



    // Animation loop

   function animate(){

    requestAnimationFrame(animate);

    if(mesh){

        mesh.rotation.z += 0.005;

    }

    renderer.render(
        scene,
        camera
    );

}

animate();


}
