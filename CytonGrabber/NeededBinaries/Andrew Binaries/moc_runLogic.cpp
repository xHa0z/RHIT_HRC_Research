/****************************************************************************
** Meta object code from reading C++ file 'runLogic.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.4.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "stdafx.h"
#include "../../include/GUI_Classes/runLogic.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'runLogic.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.4.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_RunLogic_t {
    QByteArrayData data[17];
    char stringdata[170];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_RunLogic_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_RunLogic_t qt_meta_stringdata_RunLogic = {
    {
QT_MOC_LITERAL(0, 0, 8), // "RunLogic"
QT_MOC_LITERAL(1, 9, 17), // "updateCommandList"
QT_MOC_LITERAL(2, 27, 0), // ""
QT_MOC_LITERAL(3, 28, 5), // "index"
QT_MOC_LITERAL(4, 34, 9), // "runToggle"
QT_MOC_LITERAL(5, 44, 10), // "updateMode"
QT_MOC_LITERAL(6, 55, 4), // "mode"
QT_MOC_LITERAL(7, 60, 5), // "delay"
QT_MOC_LITERAL(8, 66, 12), // "clearClicked"
QT_MOC_LITERAL(9, 79, 12), // "pauseClicked"
QT_MOC_LITERAL(10, 92, 14), // "forwardClicked"
QT_MOC_LITERAL(11, 107, 15), // "backwardClicked"
QT_MOC_LITERAL(12, 123, 10), // "runClicked"
QT_MOC_LITERAL(13, 134, 7), // "runFrom"
QT_MOC_LITERAL(14, 142, 7), // "runOnly"
QT_MOC_LITERAL(15, 150, 13), // "shapesChanged"
QT_MOC_LITERAL(16, 164, 5) // "reset"

    },
    "RunLogic\0updateCommandList\0\0index\0"
    "runToggle\0updateMode\0mode\0delay\0"
    "clearClicked\0pauseClicked\0forwardClicked\0"
    "backwardClicked\0runClicked\0runFrom\0"
    "runOnly\0shapesChanged\0reset"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_RunLogic[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      11,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    2,   69,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    2,   74,    2, 0x0a /* Public */,
       8,    0,   79,    2, 0x0a /* Public */,
       9,    0,   80,    2, 0x0a /* Public */,
      10,    0,   81,    2, 0x0a /* Public */,
      11,    0,   82,    2, 0x0a /* Public */,
      12,    0,   83,    2, 0x0a /* Public */,
      13,    1,   84,    2, 0x0a /* Public */,
      14,    1,   87,    2, 0x0a /* Public */,
      15,    0,   90,    2, 0x0a /* Public */,
      16,    0,   91,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::Int, QMetaType::QString,    3,    4,

 // slots: parameters
    QMetaType::Void, QMetaType::QString, QMetaType::Int,    6,    7,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    3,
    QMetaType::Void, QMetaType::Int,    3,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void RunLogic::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        RunLogic *_t = static_cast<RunLogic *>(_o);
        switch (_id) {
        case 0: _t->updateCommandList((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QString(*)>(_a[2]))); break;
        case 1: _t->updateMode((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 2: _t->clearClicked(); break;
        case 3: _t->pauseClicked(); break;
        case 4: _t->forwardClicked(); break;
        case 5: _t->backwardClicked(); break;
        case 6: _t->runClicked(); break;
        case 7: _t->runFrom((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 8: _t->runOnly((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: _t->shapesChanged(); break;
        case 10: _t->reset(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (RunLogic::*_t)(int , QString );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&RunLogic::updateCommandList)) {
                *result = 0;
            }
        }
    }
}

const QMetaObject RunLogic::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_RunLogic.data,
      qt_meta_data_RunLogic,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *RunLogic::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *RunLogic::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_RunLogic.stringdata))
        return static_cast<void*>(const_cast< RunLogic*>(this));
    return QObject::qt_metacast(_clname);
}

int RunLogic::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 11)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 11;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 11)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 11;
    }
    return _id;
}

// SIGNAL 0
void RunLogic::updateCommandList(int _t1, QString _t2)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_END_MOC_NAMESPACE
