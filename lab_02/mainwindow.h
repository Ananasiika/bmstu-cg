#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <QPainter>
#include <QMessageBox>

#include "objects.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_moveButton_clicked();

    void on_backButton_clicked();

    void on_cancelAllButton_clicked();

    void on_scaleButton_clicked();

    void on_rotateButton_clicked();

private:
    Ui::MainWindow *ui;
    QPixmap pxp;
    object_t horse;
    object_t origin_horse;
    std::vector<object_t> stack;
    int x = 700, y = 700;
};

#endif // MAINWINDOW_H
