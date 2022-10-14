#include <QGuiApplication>
#include <QQuickView>
#include <QOpenGLContext>
#include "Backend.h"


int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);

    QQuickView view;
    qmlRegisterType<Car>("Backend", 1, 0, "Backend");

    view.resize(1080, 720);
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.setSource(QUrl("qrc:/main.qml"));
    view.show();

    return app.exec();
}
