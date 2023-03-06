#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    horse = create_horse();
    horse = move_object(horse, (x - 700) / 2, (y - 700) / 2);
    horse.center.cords[0] = x / 2;
    horse.center.cords[1] = y / 2;
    horse = scale_object(horse, 1, -1, horse.center.cords[0], horse.center.cords[1]);
    origin_horse = horse;
    ui->setupUi(this);
    ui->label->setFixedSize(x, y);
    pxp = QPixmap(ui->label->width(), ui->label->height());
    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(horse, painter);
    ui->label->setPixmap(pxp);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_moveButton_clicked()
{
    bool ok = true;
    double dx = ui->dxEdit->text().toInt(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }
    double dy = ui->dyEdit->text().toInt(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }

    this->stack.push_back(this->horse);
    this->horse = move_object(this->horse, dx, dy);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->horse, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_backButton_clicked()
{
    this->horse = this->stack[this->stack.size() - 1];
    this->stack.pop_back();
    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->horse, painter);
    ui->label->setPixmap(pxp);

    if (this->stack.size() < 1) ui->backButton->setDisabled(true);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_cancelAllButton_clicked()
{
    this->horse = this->origin_horse;
    this->stack.clear();
    if (this->stack.size() < 1) ui->backButton->setDisabled(true);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->horse, painter);
    ui->label->setPixmap(pxp);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_scaleButton_clicked()
{
    bool ok = true;
    double kx = ui->kxEdit->text().toDouble(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }
    double ky = ui->kyEdit->text().toDouble(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }

    double xc = ui->xcScaleEdit->text().toDouble(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }
    double yc = ui->ycScaleEdit->text().toDouble(&ok);

    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }

    this->stack.push_back(this->horse);
    this->horse = scale_object(horse, kx, ky, xc, yc);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->horse, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_rotateButton_clicked()
{
    bool ok = true;
    double angle = M_PI * ui->angleEdit->text().toDouble(&ok) / 180;
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }

    double xc = ui->xcRotEdit->text().toDouble(&ok);
    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }
    double yc = ui->ycRotEdit->text().toDouble(&ok);

    if (!ok) {
        QMessageBox::warning(this, "Неверные данные", "Вы ввели неверные данные");
        return;
    }

    this->stack.push_back(this->horse);
    this->horse = rotate_object(horse, angle, xc, yc);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->horse, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр лошади ( " + QString::number(horse.center.cords[0], 'd', 0) + "; " + QString::number(horse.center.cords[1], 'd', 0) + ")");
}


