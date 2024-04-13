import QtQuick 2.15
import QtQuick.Controls 2.15

// Application window
ApplicationWindow {
    visible: true
    width: 874
    height: 540
    title: "PoGram"

    // Define variables
    property string currTime: "00:00:00"
    property QtObject backend

    // Draw rectangle filling screen
    Rectangle {
        anchors.fill: parent

        // Time in bottom left
        Text {
            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                left: parent.left
                leftMargin: 12
            }
            text: currTime
            font.pixelSize: 24
            color: "black"
        }
    }

    Connections {
        target: backend
        function onUpdated(msg) {
            currTime = msg;
        }
    }
}
