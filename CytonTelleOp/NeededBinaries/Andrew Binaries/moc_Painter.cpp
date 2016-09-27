/****************************************************************************
** Meta object code from reading C++ file 'Painter.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.4.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "stdafx.h"
#include "../../include/GUI_Classes/Painter.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'Painter.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.4.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_Painter_t {
    QByteArrayData data[22];
    char stringdata[220];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_Painter_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_Painter_t qt_meta_stringdata_Painter = {
    {
QT_MOC_LITERAL(0, 0, 7), // "Painter"
QT_MOC_LITERAL(1, 8, 4), // "save"
QT_MOC_LITERAL(2, 13, 0), // ""
QT_MOC_LITERAL(3, 14, 11), // "std::string"
QT_MOC_LITERAL(4, 26, 15), // "projectLocation"
QT_MOC_LITERAL(5, 42, 4), // "load"
QT_MOC_LITERAL(6, 47, 9), // "loadRobot"
QT_MOC_LITERAL(7, 57, 13), // "robotLocation"
QT_MOC_LITERAL(8, 71, 14), // "loadPhotoCanny"
QT_MOC_LITERAL(9, 86, 7), // "cv::Mat"
QT_MOC_LITERAL(10, 94, 5), // "image"
QT_MOC_LITERAL(11, 100, 9), // "threshold"
QT_MOC_LITERAL(12, 110, 15), // "min_line_length"
QT_MOC_LITERAL(13, 126, 15), // "loadPhotoKmeans"
QT_MOC_LITERAL(14, 142, 10), // "colorCount"
QT_MOC_LITERAL(15, 153, 13), // "minRegionSize"
QT_MOC_LITERAL(16, 167, 10), // "newClicked"
QT_MOC_LITERAL(17, 178, 6), // "resize"
QT_MOC_LITERAL(18, 185, 4), // "int*"
QT_MOC_LITERAL(19, 190, 5), // "width"
QT_MOC_LITERAL(20, 196, 6), // "height"
QT_MOC_LITERAL(21, 203, 16) // "murderousRampage"

    },
    "Painter\0save\0\0std::string\0projectLocation\0"
    "load\0loadRobot\0robotLocation\0"
    "loadPhotoCanny\0cv::Mat\0image\0threshold\0"
    "min_line_length\0loadPhotoKmeans\0"
    "colorCount\0minRegionSize\0newClicked\0"
    "resize\0int*\0width\0height\0murderousRampage"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_Painter[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   54,    2, 0x0a /* Public */,
       5,    1,   57,    2, 0x0a /* Public */,
       6,    1,   60,    2, 0x0a /* Public */,
       8,    3,   63,    2, 0x0a /* Public */,
      13,    3,   70,    2, 0x0a /* Public */,
      16,    0,   77,    2, 0x0a /* Public */,
      17,    2,   78,    2, 0x0a /* Public */,
      21,    0,   83,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 3,    4,
    QMetaType::Void, 0x80000000 | 3,    4,
    QMetaType::Void, 0x80000000 | 3,    7,
    QMetaType::Void, 0x80000000 | 9, QMetaType::Int, QMetaType::Int,   10,   11,   12,
    QMetaType::Void, 0x80000000 | 9, QMetaType::Int, QMetaType::Int,   10,   14,   15,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 18, 0x80000000 | 18,   19,   20,
    QMetaType::Void,

       0        // eod
};

void Painter::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        Painter *_t = static_cast<Painter *>(_o);
        switch (_id) {
        case 0: _t->save((*reinterpret_cast< std::string(*)>(_a[1]))); break;
        case 1: _t->load((*reinterpret_cast< std::string(*)>(_a[1]))); break;
        case 2: _t->loadRobot((*reinterpret_cast< std::string(*)>(_a[1]))); break;
        case 3: _t->loadPhotoCanny((*reinterpret_cast< cv::Mat(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 4: _t->loadPhotoKmeans((*reinterpret_cast< cv::Mat(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 5: _t->newClicked(); break;
        case 6: _t->resize((*reinterpret_cast< int*(*)>(_a[1])),(*reinterpret_cast< int*(*)>(_a[2]))); break;
        case 7: _t->murderousRampage(); break;
        default: ;
        }
    }
}

const QMetaObject Painter::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_Painter.data,
      qt_meta_data_Painter,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *Painter::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *Painter::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_Painter.stringdata))
        return static_cast<void*>(const_cast< Painter*>(this));
    return QObject::qt_metacast(_clname);
}

int Painter::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 8;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
