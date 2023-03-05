#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    bun = create_bun();
    bun = scale_object(bun, 1, -1, bun.center.cords[0], bun.center.cords[1]);
    origin_bun = bun;
    ui->setupUi(this);
    pxp = QPixmap(ui->label->width(), ui->label->height());
    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(bun, painter);
    ui->label->setPixmap(pxp);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
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

    this->stack.push_back(this->bun);
    this->bun = move_object(this->bun, dx, dy);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->bun, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_backButton_clicked()
{
    this->bun = this->stack[this->stack.size() - 1];
    this->stack.pop_back();
    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->bun, painter);
    ui->label->setPixmap(pxp);

    if (this->stack.size() < 1) ui->backButton->setDisabled(true);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
}

void MainWindow::on_cancelAllButton_clicked()
{
    this->bun = this->origin_bun;
    this->stack.clear();
    if (this->stack.size() < 1) ui->backButton->setDisabled(true);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->bun, painter);
    ui->label->setPixmap(pxp);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
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

    this->stack.push_back(this->bun);
    this->bun = scale_object(bun, kx, ky, xc, yc);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->bun, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
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

    this->stack.push_back(this->bun);
    this->bun = rotate_object(bun, angle, xc, yc);

    pxp.fill();
    QPainter painter(&pxp);
    QPen pen;
    pen.setWidth(4);
    painter.setPen(pen);
    draw_object(this->bun, painter);
    ui->label->setPixmap(pxp);
    ui->backButton->setEnabled(true);
    ui->centerLabel->setText("Центр ( " + QString::number(bun.center.cords[0], 'd', 0) + "; " + QString::number(bun.center.cords[1], 'd', 0) + ")");
}
