#ifndef BACKEND_H
#define BACKEND_H

#include <QObject>
#include <QString>
#include <QVector3D>

class Car : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString translation READ translation WRITE setTranslation NOTIFY translationChanged)

public:
    Car() {}
    virtual ~Car() {}

    QString translation();
    void setTranslation(const QString &translation);

signals:
    void translationChanged();

private:
    QString m_translation;
};

#endif // BACKEND_H
