import QtQuick 2.1 as QQ2
import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0
import QtQuick 2.15
//import "Movement.js" as Move
import Backend 1.0

import QtQuick.Controls 2.12

Entity {
    id: sceneRoot

    //property alias trsl: trefoil.trans


    Camera {
        id: camera
        projectionType: CameraLens.PerspectiveProjection
        fieldOfView: 90
        //aspectRatio: _window.width / _window.height
        nearPlane: 0.1
        farPlane: 1000.0
        position: Qt.vector3d(0.0, 3.0, -2.0)
        viewCenter: Qt.vector3d(0.0, 2.0, 0.0)
        upVector: Qt.vector3d(0.0, 1.0, 0.0)
    }

    FirstPersonCameraController { camera: camera }

    ShadowMapLight {
        id: light
    }

    components: [
        ShadowMapFrameGraph {
            id: framegraph
            viewCamera: camera
            lightCamera: light.lightCamera
        },
        // Event Source will be set by the Qt3DQuickWindow
        InputSettings { }

    ]


    AdsEffect {
        id: shadowMapEffect
        shadowTexture: framegraph.shadowTexture
        light: light
    }

    // Toyplane entity
    MainCar {
        material: AdsMaterial {
            effect: shadowMapEffect
            diffuseColor: Qt.rgba(0.18, 0.56, 0.99, 1.0)
            shininess: 75
        }
    }

    // Plane entity
    GroundPlane {
        material: AdsMaterial {
            effect: shadowMapEffect
            diffuseColor: Qt.rgba(0.99, 0.98, 0.98, 1.0)
            specularColor: Qt.rgba(0, 0, 0, 1.0)
        }
    }

//    Trefoil {
//        id: trefoil
//        //trans:  Qt.vector3d(5, 2, 2)
//    }

    WorkerScript {
        id: worker
        source: "script.mjs"

        onMessage: {
            backend.translation = (Number(backend.translation) + 0.03).toString()
            console.log("yes")

            var count = 0;
            var Component = Qt.createComponent("Trefoil.qml");
            var car = Component.createObject(sceneRoot);

            if (car == null){
                console.log("Error creating a car");
            }else{
                console.log("created...");
                car.trans = Qt.vector3d(Number(backend.translation), 2, Number(backend.translation));
            }

            car.destroy(50);
            console.log("destroyed...");
            count++;
        }
    }

    Timer {
        id: timer
        interval: 40; repeat: true
        running: true
        triggeredOnStart: true

        onTriggered: {
            var msg = {'action': 'appendCurrentTime'};
            worker.sendMessage(msg);
        }
    }

}
