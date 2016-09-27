/****************************************************************************
** Meta object code from reading C++ file 'CommandWindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.4.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "stdafx.h"
#include "../../include/GUI_Classes/CommandWindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'CommandWindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.4.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_CommandWindow_t {
    QByteArrayData data[34];
    char stringdata[378];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_CommandWindow_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_CommandWindow_t qt_meta_stringdata_CommandWindow = {
    {
QT_MOC_LITERAL(0, 0, 13), // "CommandWindow"
QT_MOC_LITERAL(1, 14, 15), // "modifiedCommand"
QT_MOC_LITERAL(2, 30, 0), // ""
QT_MOC_LITERAL(3, 31, 14), // "highlightShape"
QT_MOC_LITERAL(4, 46, 5), // "index"
QT_MOC_LITERAL(5, 52, 7), // "runFrom"
QT_MOC_LITERAL(6, 60, 7), // "runOnly"
QT_MOC_LITERAL(7, 68, 11), // "modeUpdated"
QT_MOC_LITERAL(8, 80, 4), // "mode"
QT_MOC_LITERAL(9, 85, 5), // "delay"
QT_MOC_LITERAL(10, 91, 13), // "moveUpClicked"
QT_MOC_LITERAL(11, 105, 15), // "moveDownClicked"
QT_MOC_LITERAL(12, 121, 20), // "deleteCommandClicked"
QT_MOC_LITERAL(13, 142, 16), // "launchRightClick"
QT_MOC_LITERAL(14, 159, 1), // "p"
QT_MOC_LITERAL(15, 161, 8), // "menuSort"
QT_MOC_LITERAL(16, 170, 8), // "QAction*"
QT_MOC_LITERAL(17, 179, 1), // "a"
QT_MOC_LITERAL(18, 181, 10), // "cellChange"
QT_MOC_LITERAL(19, 192, 6), // "curRow"
QT_MOC_LITERAL(20, 199, 6), // "curCol"
QT_MOC_LITERAL(21, 206, 7), // "prevRow"
QT_MOC_LITERAL(22, 214, 7), // "prevCol"
QT_MOC_LITERAL(23, 222, 10), // "updateMode"
QT_MOC_LITERAL(24, 233, 18), // "disableModeSetting"
QT_MOC_LITERAL(25, 252, 17), // "enableModeSetting"
QT_MOC_LITERAL(26, 270, 14), // "drawingStarted"
QT_MOC_LITERAL(27, 285, 13), // "drawingPaused"
QT_MOC_LITERAL(28, 299, 14), // "drawingCleared"
QT_MOC_LITERAL(29, 314, 8), // "showTime"
QT_MOC_LITERAL(30, 323, 20), // "colorChangeConfirmed"
QT_MOC_LITERAL(31, 344, 8), // "populate"
QT_MOC_LITERAL(32, 353, 17), // "updateCommandList"
QT_MOC_LITERAL(33, 371, 6) // "toggle"

    },
    "CommandWindow\0modifiedCommand\0\0"
    "highlightShape\0index\0runFrom\0runOnly\0"
    "modeUpdated\0mode\0delay\0moveUpClicked\0"
    "moveDownClicked\0deleteCommandClicked\0"
    "launchRightClick\0p\0menuSort\0QAction*\0"
    "a\0cellChange\0curRow\0curCol\0prevRow\0"
    "prevCol\0updateMode\0disableModeSetting\0"
    "enableModeSetting\0drawingStarted\0"
    "drawingPaused\0drawingCleared\0showTime\0"
    "colorChangeConfirmed\0populate\0"
    "updateCommandList\0toggle"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_CommandWindow[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      21,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       5,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,  119,    2, 0x06 /* Public */,
       3,    1,  120,    2, 0x06 /* Public */,
       5,    1,  123,    2, 0x06 /* Public */,
       6,    1,  126,    2, 0x06 /* Public */,
       7,    2,  129,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      10,    0,  134,    2, 0x08 /* Private */,
      11,    0,  135,    2, 0x08 /* Private */,
      12,    0,  136,    2, 0x08 /* Private */,
      13,    1,  137,    2, 0x08 /* Private */,
      15,    1,  140,    2, 0x08 /* Private */,
      18,    4,  143,    2, 0x08 /* Private */,
      23,    0,  152,    2, 0x08 /* Private */,
      24,    0,  153,    2, 0x08 /* Private */,
      25,    0,  154,    2, 0x08 /* Private */,
      26,    0,  155,    2, 0x08 /* Private */,
      27,    0,  156,    2, 0x08 /* Private */,
      28,    0,  157,    2, 0x08 /* Private */,
      29,    0,  158,    2, 0x08 /* Private */,
      30,    0,  159,    2, 0x08 /* Private */,
      31,    0,  160,    2, 0x0a /* Public */,
      32,    2,  161,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    4,
    QMetaType::Void, QMetaType::Int,    4,
    QMetaType::Void, QMetaType::Int,    4,
    QMetaType::Void, QMetaType::QString, QMetaType::Int,    8,    9,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QPoint,   14,
    QMetaType::Void, 0x80000000 | 16,   17,
    QMetaType::Void, QMetaType::Int, QMetaType::Int, QMetaType::Int, QMetaType::Int,   19,   20,   21,   22,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, QMetaType::QString,    4,   33,

       0        // eod
};

void CommandWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        CommandWindow *_t = static_cast<CommandWindow *>(_o);
        switch (_id) {
        case 0: _t->modifiedCommand(); break;
        case 1: _t->highlightShape((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 2: _t->runFrom((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->runOnly((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: _t->modeUpdated((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 5: _t->moveUpClicked(); break;
        case 6: _t->moveDownClicked(); break;
        case 7: _t->deleteCommandClicked(); break;
        case 8: _t->launchRightClick((*reinterpret_cast< QPoint(*)>(_a[1]))); break;
        case 9: _t->menuSort((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 10: _t->cellChange((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4]))); break;
        case 11: _t->updateMode(); break;
        case 12: _t->disableModeSetting(); break;
        case 13: _t->enableModeSetting(); break;
        case 14: _t->drawingStarted(); break;
        case 15: _t->drawingPaused(); break;
        case 16: _t->drawingCleared(); break;
        case 17: _t->showTime(); break;
        case 18: _t->colorChangeConfirmed(); break;
        case 19: _t->populate(); break;
        case 20: _t->updateCommandList((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QString(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 9:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (CommandWindow::*_t)();
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&CommandWindow::modifiedCommand)) {
                *result = 0;
            }
        }
        {
            typedef void (CommandWindow::*_t)(int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&CommandWindow::highlightShape)) {
                *result = 1;
            }
        }
        {
            typedef void (CommandWindow::*_t)(int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&CommandWindow::runFrom)) {
                *result = 2;
            }
        }
        {
            typedef void (CommandWindow::*_t)(int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&CommandWindow::runOnly)) {
                *result = 3;
            }
        }
        {
            typedef void (CommandWindow::*_t)(QString , int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&CommandWindow::modeUpdated)) {
                *result = 4;
            }
        }
    }
}

const QMetaObject CommandWindow::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_CommandWindow.data,
      qt_meta_data_CommandWindow,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *CommandWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *CommandWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_CommandWindow.stringdata))
        return static_cast<void*>(const_cast< CommandWindow*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int CommandWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 21)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 21;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 21)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 21;
    }
    return _id;
}

// SIGNAL 0
void CommandWindow::modifiedCommand()
{
    QMetaObject::activate(this, &staticMetaObject, 0, Q_NULLPTR);
}

// SIGNAL 1
void CommandWindow::highlightShape(int _t1)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void CommandWindow::runFrom(int _t1)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void CommandWindow::runOnly(int _t1)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void CommandWindow::modeUpdated(QString _t1, int _t2)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)) };
    QMetaObject::activate(this, &staticMetaObject, 4, _a);
}
QT_END_MOC_NAMESPACE
