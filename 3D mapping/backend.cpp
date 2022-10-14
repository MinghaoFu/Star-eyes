#include "Backend.h"

QString Car::translation(){
    return m_translation;
}

void Car::setTranslation(const QString &translation){
    if (m_translation == translation)
        return;

    m_translation = translation;
    emit translationChanged();
}
