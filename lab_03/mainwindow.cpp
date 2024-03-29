#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "algorithms.h"
#include <QColorDialog>
#include <QColor>
#include <QMessageBox>
#include <QWheelEvent>
#include <iostream>
#include <QTimer>
#include <QDrag>
#include <QMimeData>
#include <QtGlobal>
#include <cmath>
#include <fstream>

#define DEF_X ui->graphicsView->geometry().x() / 2.0
#define DEF_Y ui->graphicsView->geometry().y() / 2.0;
#define DEF_R 350
#define DEF_ANGLE 1

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QAction *AboutProgAction = ui->menubar->addAction("О программе");
    connect(AboutProgAction, SIGNAL(triggered()), this, SLOT(app_info_show()));
    QAction *AboutAuthorAction = ui->menubar->addAction("Об авторе");
    connect(AboutAuthorAction, SIGNAL(triggered()), this, SLOT(author_info_show()));
    QAction *ExitAction = ui->menubar->addAction(("Выход"));
    connect(ExitAction, SIGNAL(triggered()), this, SLOT(exit_show()));


    scene = new QGraphicsScene();
    ui->graphicsView->setScene(scene);
    ui->graphicsView->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    ui->graphicsView->setRenderHint(QPainter::Antialiasing, false);
    ui->pushButton_cancel->setEnabled(false);

    data.back_color = Qt::white;
    show_color(data.back_color, ui->label_bc);
    show_color(line_color, ui->label_lc);

    ui->graphicsView->viewport()->installEventFilter(this);
    ui->graphicsView->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    ui->graphicsView->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    ui->graphicsView->setDragMode(QGraphicsView::ScrollHandDrag);
}

MainWindow::~MainWindow()
{
    delete ui;
    delete scene;
    cancel = std::stack <content_t>();
}

void MainWindow::showEvent(QShowEvent *ev)
{
    QMainWindow::showEvent(ev);
    QTimer::singleShot(500, this, SLOT(windowShown()));
}

void MainWindow::windowShown()
{
    drawing_content();
}

static void copy(struct content_t **a, struct content_t *b)
{
    for (size_t i = 0; i < b->lines.size(); i++)
        (*a)->lines.push_back(b->lines[i]);

    for (size_t i = 0; i < b->spectrums.size(); i++)
        (*a)->spectrums.push_back(b->spectrums[i]);

    (*a)->back_color = b->back_color;
}

// информационные функции
void MainWindow::app_info_show()
{
    QMessageBox::information(NULL, "О программе","Реализация и исследование алгоритмов построения отрезков");
}

void MainWindow::author_info_show()
{
    QMessageBox::information(NULL, "Об авторе", "Пронина Лариса ИУ7-44Б");
}

void MainWindow::exit_show()
{
    QMessageBox msg_quit;
    msg_quit.setText("Работа с программой будет завершена");
    msg_quit.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
    msg_quit.setIcon(QMessageBox::Warning);
    msg_quit.setDefaultButton(QMessageBox::Ok);
    msg_quit.setWindowTitle("Предупреждение!");
    int rc = msg_quit.exec();

    if (rc == QMessageBox::Ok)
        qApp->quit();
}

// вывод предупреждений
void MainWindow::print_warning(QString str)
{
    QMessageBox::information(NULL, "Ошибка!", str);
}

// функция события колесика мыши
void MainWindow::wheelEvent(QWheelEvent* event)
{
    ui->graphicsView->setTransformationAnchor(QGraphicsView::AnchorUnderMouse);
    double scale_factor = 1.15;
    if (event->angleDelta().y() > 0)
        ui->graphicsView->scale(scale_factor, scale_factor);
    else
        ui->graphicsView->scale(1 / scale_factor, 1 / scale_factor);
}

bool MainWindow::eventFilter(QObject* object, QEvent* event)
{
    if (event->type() == QEvent::Wheel && object == ui->graphicsView->viewport())
    {
#if QT_VERSION >= 0x060000
        QWheelEvent *wheel_event = static_cast<QWheelEvent *>(event);
        wheelEvent(wheel_event);
#endif
        return true;
    }
    return false;
}

void MainWindow::drawing_axes()
{
    QPen pen = QPen(Qt::black, 1);
    // Oy
    scene->addLine(0, -10, 0, 200, pen);
    scene->addLine(0, 200, 10, 185, pen);
    scene->addLine(0, 200, -10, 185, pen);
    // Y
    scene->addLine(-6, 210, 0, 220, pen);
    scene->addLine(0, 220, 6, 210, pen);
    scene->addLine(0, 220, 0, 228, pen);

    // Ox
    scene->addLine(-10, 0, 200, 0, pen);
    scene->addLine(200, 0, 185, 10, pen);
    scene->addLine(200, 0, 185, -10, pen);
    // X
    scene->addLine(210, -6, 218, 6, pen);
    scene->addLine(218, -6, 210, 6, pen);
}

// функции рисования
void MainWindow::drawing_content()
{
    scene->clear();
    ui->graphicsView->setBackgroundBrush(data.back_color);
    drawing_axes();
    for (size_t i = 0; i < data.lines.size(); i++)
        drawing_line(data.lines[i], true, false);

    for (size_t i = 0; i < data.spectrums.size(); i++)
        drawing_spectrum(data.spectrums[i]);
}

// рисование линий
int MainWindow::drawing_line(line_t &line, bool is_drawing, bool is_cnt_steps)
{
    int rc = 0;
    switch (line.method)
    {
        case STANDART:
            standart_line(line, ui->graphicsView->scene());
            break;
        case DDA:
            rc = dda_line(line, ui->graphicsView->scene(), is_drawing, is_cnt_steps);
            break;
        case BRESEN_INT:
            rc = bresen_int_line(line, ui->graphicsView->scene(), is_drawing, is_cnt_steps);
            break;
        case BRESEN_DOUBLE:
            rc = bresen_double_line(line, ui->graphicsView->scene(), is_drawing, is_cnt_steps);
            break;
        case BRESEN_STEPS:
            rc = bresen_steps_line(line, ui->graphicsView->scene(), is_drawing, is_cnt_steps);
            break;
        case WY:
            rc = wy_line(line, ui->graphicsView->scene(), is_drawing, is_cnt_steps);
            break;
    }
    if (is_cnt_steps)
        return rc;
    return -1;
}

// функция рисования спектра
void MainWindow::drawing_spectrum(spectrum_t &spectrum)
{
    double x, y;
    QPointF cur_end;
    line_t line;
    line.color = spectrum.color;
    line.method = spectrum.method;
    line.start = spectrum.center;
    for (double i = 0.0; i <= 360.0; i += spectrum.angle)
    {
        x = spectrum.center.x() + cos(M_PI * i / 180) * spectrum.radius;
        y = spectrum.center.y() + sin(M_PI * i / 180) * spectrum.radius;
        cur_end = QPointF(x, y);
        line.end = cur_end;
        drawing_line(line, true, false);
    }
}

// показать цвет на лейбл
void MainWindow::show_color(QColor color, QLabel *lab)
{
    QImage im = QImage(lab->geometry().width(), lab->geometry().height(), QImage::Format_RGB32);
    QPainter p(&im);
    p.setBrush(QBrush(color));
    p.setPen(Qt::black);
    QRect rect = QRect(0, 0, lab->geometry().width(), lab->geometry().height());
    p.drawRect(rect);

    QPixmap pixmap = QPixmap::fromImage(im);
    lab->clear();
    lab->setPixmap(pixmap);
}

// выбор цвета фона
void MainWindow::on_pushButton_back_color_clicked()
{
    QColorDialog dialog;
    dialog.setCurrentColor(data.back_color);
    dialog.show();
    dialog.exec();
    QColor color = dialog.selectedColor();
    if (!color.isValid())
        print_warning("Что-то пошло не так");
    else
        back_color = color;
    show_color(back_color, ui->label_bc);
}

// выбор цвета линий
void MainWindow::on_pushButton_line_color_clicked()
{
    QColorDialog dialog;
    dialog.setCurrentColor(line_color);
    dialog.show();
    dialog.exec();
    QColor color = dialog.selectedColor();
    if (!color.isValid())
        print_warning("Что-то пошло не так");
    else
        line_color = color;
    show_color(line_color, ui->label_lc);
}

// построить линию
void MainWindow::on_pushButton_line_clicked()
{
    QString str_x_start = ui->lineEdit_line_x_start->text();
    QString str_y_start = ui->lineEdit_line_y_start->text();
    QString str_x_end = ui->lineEdit_line_x_end->text();
    QString str_y_end = ui->lineEdit_line_y_end->text();

    if (str_x_end.length() == 0 || str_x_start.length() == 0 || str_y_end.length() == 0 || str_y_start.length() == 0)
        print_warning("Ошибка ввода: пустой или неполный ввод");
    else
    {
        bool flag_x_start, flag_y_start, flag_x_end, flag_y_end;
        double x_start, y_start, x_end, y_end;
        x_start = str_x_start.toDouble(&flag_x_start);
        y_start = str_y_start.toDouble(&flag_y_start);
        x_end = str_x_end.toDouble(&flag_x_end);
        y_end = str_y_end.toDouble(&flag_y_end);
        if (!flag_x_start || !flag_x_end || !flag_y_start || !flag_y_end)
            print_warning("Ошибка ввода: Некорректный ввод");
        else
        {
            QPointF start, end;
            start = QPointF(x_start, y_start);
            end = QPointF(x_end, y_end);

            if (start == end)
                print_warning("Ошибка ввода: Точки начала и конца отрезка совпадают");
            else
            {
                content_t *c = new content_t;
                copy(&c, &data);
                cancel.push(*c);
                ui->pushButton_cancel->setEnabled(true);

                line_t line;
                line.color = line_color;
                line.method = (method_t) ui->comboBox->currentIndex();
                line.start = start;
                line.end = end;
                data.lines.push_back(line);
                drawing_line(line, true, false);
                data.back_color = back_color;
                ui->graphicsView->setBackgroundBrush(back_color);
            }
        }
    }
}

// построить спектр
void MainWindow::on_pushButton_spectrum_clicked()
{
    QString str_spectrum_x = ui->lineEdit_spectrum_x->text();
    QString str_spectrum_y = ui->lineEdit_spectrum_y->text();
    QString str_spectrum_r = ui->lineEdit_spectrum_radius->text();
    QString str_angle = ui->lineEdit_angle->text();

    if (str_spectrum_x.length() == 0 || str_spectrum_y.length() == 0 || str_spectrum_r.length() == 0 || str_angle.length() == 0)
        print_warning("Ошибка ввода: пустой или неполный ввод");
    else
    {
        bool flag_spectrum_x, flag_spectrum_y, flag_spectrum_r, flag_angle;
        double spectrum_x, spectrum_y;
        double spectrum_r, angle;

        spectrum_x = str_spectrum_x.toDouble(&flag_spectrum_x);
        spectrum_y = str_spectrum_y.toDouble(&flag_spectrum_y);
        spectrum_r = str_spectrum_r.toDouble(&flag_spectrum_r);
        angle = str_angle.toDouble(&flag_angle);

        if (!flag_spectrum_x || !flag_spectrum_y || !flag_spectrum_r || !flag_angle)
            print_warning("Ошибка ввода: некорректный ввод");
        else
        {
            content_t *c = new content_t;
            copy(&c, &data);
            cancel.push(*c);
            ui->pushButton_cancel->setEnabled(true);

            QPointF center = QPointF(spectrum_x, spectrum_y);

            spectrum_t spectrum;
            spectrum.center = center;
            spectrum.angle = angle;
            spectrum.color = line_color;
            spectrum.method = (method_t) ui->comboBox->currentIndex();
            spectrum.radius = spectrum_r;
            data.spectrums.push_back(spectrum);
            data.back_color = back_color;
            ui->graphicsView->setBackgroundBrush(back_color);
            drawing_spectrum(spectrum);
        }
    }
}

// функция очистки всего холста
void MainWindow::on_pushButton_clear_clicked()
{
    data.back_color = Qt::white;
    line_color = Qt::black;
    show_color(data.back_color, ui->label_bc);
    show_color(line_color, ui->label_lc);
    data.lines.clear();
    data.spectrums.clear();
    cancel = std::stack<content_t>();
    ui->graphicsView->resetTransform();
    drawing_content();
    ui->pushButton_cancel->setEnabled(false);
}

// функция отмены действия
void MainWindow::on_pushButton_cancel_clicked()
{
    if (!cancel.empty())
    {
        data = cancel.top();
        cancel.pop();
        drawing_content();
    }
    if (cancel.empty())
        ui->pushButton_cancel->setEnabled(false);
}

// изменение размера (все перестроится)
void MainWindow::resizeEvent(QResizeEvent* event)
{
    QMainWindow::resizeEvent(event);
    ui->graphicsView->resetTransform();
    drawing_content();
}

void MainWindow::on_pushButton_reset_scale_clicked()
{
    ui->graphicsView->resetTransform();
}

void MainWindow::measure_steps(spectrum_t spectrum, std::vector<int> &all_steps)
{
    double x, y;
    QPointF cur_end;
    line_t line;
    line.color = spectrum.color;
    line.method = spectrum.method;
    line.start = spectrum.center;
    int step;
    for (double j = 0.0; j <= 90.0; j += spectrum.angle)
    {
        x = spectrum.center.x() + cos(M_PI * j / 180) * spectrum.radius;
        y = spectrum.center.y() + sin(M_PI * j / 180) * spectrum.radius;
        cur_end = QPointF(x, y);
        line.end = cur_end;
        step = drawing_line(line, false, true);
        all_steps.push_back(step);
    }
}

// кол-во ступенек в зависимости от угла
void MainWindow::on_pushButton_steps_clicked()
{
    QString str_spectrum_x = ui->lineEdit_spectrum_x->text();
    QString str_spectrum_y = ui->lineEdit_spectrum_y->text();
    QString str_spectrum_r = ui->lineEdit_spectrum_radius->text();
    QString str_angle = ui->lineEdit_angle->text();

    bool flag_spectrum_x, flag_spectrum_y, flag_spectrum_r, flag_angle;
    double spectrum_x, spectrum_y;
    double spectrum_r, angle;

    spectrum_x = str_spectrum_x.toDouble(&flag_spectrum_x);
    spectrum_y = str_spectrum_y.toDouble(&flag_spectrum_y);
    spectrum_r = str_spectrum_r.toDouble(&flag_spectrum_r);
    angle = str_angle.toDouble(&flag_angle);

    if (!flag_spectrum_x)
        spectrum_x = DEF_X;
    if (!flag_spectrum_y)
        spectrum_y = DEF_Y;
    if (!flag_spectrum_r)
        spectrum_r = DEF_R;
    if (!flag_angle)
        angle = DEF_ANGLE;

    QPointF center = QPointF(spectrum_x, spectrum_y);

    spectrum_t spectrum;
    spectrum.center = center;
    spectrum.angle = angle;
    spectrum.color = line_color;
    spectrum.radius = spectrum_r;
    std::vector<int> steps;
    spectrum.method = DDA;
    measure_steps(spectrum, steps);
    spectrum.method = BRESEN_DOUBLE;
    measure_steps(spectrum, steps);
    spectrum.method = BRESEN_INT;
    measure_steps(spectrum, steps);
    spectrum.method = BRESEN_STEPS;
    measure_steps(spectrum, steps);
    spectrum.method = WY;
    measure_steps(spectrum, steps);

    double ma = spectrum.angle * std::ceil(90 / spectrum.angle);
    std::ofstream out("../lab_03/steps_res.txt");

    if (out.is_open())
    {
        out << spectrum.radius << "\n";
        out << spectrum.angle << "\n";
        out << ma << "\n";
        for (std::size_t i = 0; i < steps.size(); i++)
            out << steps[i] << "\n";
    }
    out.close();
        system("python3 ../lab_03/steps.py");

}

double MainWindow::measure_avg_time(spectrum_t spectrum)
{
    const int iterations = 100;
    using std::chrono::duration;
    using std::chrono::duration_cast;
    using std::chrono::high_resolution_clock;
    using std::chrono::microseconds;

    auto end = high_resolution_clock::now();
    auto start = high_resolution_clock::now();
    double x, y;
    QPointF cur_end;
    line_t line;
    line.color = spectrum.color;
    line.method = spectrum.method;
    line.start = spectrum.center;

    for (int i = 0; i < iterations; i++)
    {
        for (double j = 0.0; j <= 360.0; j += spectrum.angle)
        {
            x = spectrum.center.x() + cos(M_PI * j / 180) * spectrum.radius;
            y = spectrum.center.y() + sin(M_PI * j / 180) * spectrum.radius;
            cur_end = QPointF(x, y);
            line.end = cur_end;
            drawing_line(line, false, false);
        }
    }
    end = high_resolution_clock::now();
    return (double)duration_cast<microseconds>(end - start).count() / iterations;
}

// время выполнения
void MainWindow::on_pushButton_time_clicked()
{
    QString str_spectrum_x = ui->lineEdit_spectrum_x->text();
    QString str_spectrum_y = ui->lineEdit_spectrum_y->text();
    QString str_spectrum_r = ui->lineEdit_spectrum_radius->text();
    QString str_angle = ui->lineEdit_angle->text();

    bool flag_spectrum_x, flag_spectrum_y, flag_spectrum_r, flag_angle;
    double spectrum_x, spectrum_y;
    double spectrum_r, angle;

    spectrum_x = str_spectrum_x.toDouble(&flag_spectrum_x);
    spectrum_y = str_spectrum_y.toDouble(&flag_spectrum_y);
    spectrum_r = str_spectrum_r.toDouble(&flag_spectrum_r);
    angle = str_angle.toDouble(&flag_angle);

    if (!flag_spectrum_x)
        spectrum_x = DEF_X;
    if (!flag_spectrum_y)
        spectrum_y = DEF_Y;
    if (!flag_spectrum_r)
        spectrum_r = DEF_R;
    if (!flag_angle)
        angle = DEF_ANGLE;
    QPointF center = QPointF(spectrum_x, spectrum_y);

    spectrum_t spectrum;
    spectrum.center = center;
    spectrum.angle = angle;
    spectrum.color = line_color;
    spectrum.radius = spectrum_r;

    std::vector<double> time;
    for (int i = DDA; i <= WY; i++)
    {
        spectrum.method = (method_t) i;
        time.push_back(measure_avg_time(spectrum));
    }

    std::ofstream out("../lab_03/time_res.txt");

    if (out.is_open())
    {
        out << spectrum.radius << "\n";
        for (std::size_t i = 0; i < time.size(); i++)
            out << time[i] << "\n";
    }
    out.close();
    system("python3 ../lab_03/time.py");
}
