import QtQuick 2.0
import Backend 1.0

Item {
    Backend{
        id: backend
        onTranslationChanged: console.log(backend.translation)


    }
}
