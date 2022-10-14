import QtQuick 2.0
import QtQuick.Scene3D 2.0
import Qt3D.Render 2.0
import QtQuick.Controls 2.12
import Qt3D.Core 2.0
import Backend 1.0

Item {
    //property alias y: backend.translation

    Backend{
        id: backend
        onTranslationChanged: console.log(backend.translation)
    }

//    WorkerScript {
//        id: worker
//        source: "script.mjs"

//        onMessage: {
//            backend.translation = (Number(backend.translation) + 0.03).toString()
//            console.log("yes")

//            var count = 0;
//            var Component = Qt.createComponent("Trefoil.qml");
//            var car = Component.createObject(sceneRoot, {trans: Qt.vector3d(0, 2, 2)});

//            if (car == null){
//                console.log("Error creating a car");
//            }else{
//                console.log("created...");
//                //car.trans = Qt.vector3d(-4 + 0.2*count, 2, 2);
//            }

//            //sleep(2000);
//            car.destroy(2000);
//            console.log("destroyed...");
//            count++;
//        }
//    }

//    Timer {
//        id: timer
//        interval: 40; repeat: true
//        running: true
//        triggeredOnStart: true

//        onTriggered: {
//            var msg = {'action': 'appendCurrentTime'};
//            worker.sendMessage(msg);
//        }
//    }

    Rectangle {
        id: scene
        property bool colorChange: true
        anchors.fill: parent
        color: "#2d2d2d"

        Rectangle {
            id: controlsbg
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.topMargin: 10
            anchors.rightMargin: 900
            anchors.bottomMargin: 10
            color: "grey"
            Column {
                spacing: 10
                anchors.centerIn: parent

                TextField {
                    width: 150;
                    placeholderText: qsTr("User name")
                    onTextChanged: {
                        backend.translation = text
                    }
                }

                Label {
                    text: backend.translation
                    width: 150;
                    font.pointSize: 20
                    background: Rectangle {
                        color: "lightgrey"
                    }
                }
            }



        }

        Scene3D {
            id: scene3d
            anchors.fill: parent
            anchors.leftMargin: 200
            anchors.topMargin: 10
            anchors.rightMargin: 10
            anchors.bottomMargin: 10
            focus: true
            aspects: ["input", "logic"]
            cameraAspectRatioMode: Scene3D.AutomaticAspectRatio

            SceneRoot {
                id: sceneRoot
            }
        }



    }
}
