#ifndef OBJECTS_H
#define OBJECTS_H

#include <QPainter>

#include <vector>
#include <math.h>

#include "matrix_funcs.h"

struct point_t {
    std::vector<double> cords;
};

point_t point(double x, double y);

struct edge_t {
    point_t p1;
    point_t p2;
};

struct point_figure_t {
    std::vector<point_t> points;
};

struct linear_figure_t {
    std::vector<edge_t> edges;
};

struct object_t {
    std::vector<point_figure_t> point_figures;
    std::vector<linear_figure_t> linear_figures;

    point_t center;
};

void draw_point(point_t p, QPainter &painter);
void draw_edge(edge_t e, QPainter &painter);
void draw_linear(linear_figure_t f, QPainter &painter);
void draw_points(point_figure_t f, QPainter &painter);
void draw_object(object_t o, QPainter &painter);

linear_figure_t create_line(point_t a, point_t b);
linear_figure_t create_triangle(point_t a, point_t b, point_t c);
linear_figure_t create_ellips(point_t a,  point_t b, int points);
object_t create_bun();

point_t move_point(point_t p, double dx, double dy);
edge_t move_edge(edge_t e, double dx, double dy);
linear_figure_t move_linear(linear_figure_t f, double dx, double dy);
point_figure_t move_points(point_figure_t f, double dx, double dy);
object_t move_object(object_t o, double dx, double dy);

point_t scale_point_c(point_t p, double kx, double ky);
point_t scale_point(point_t p, double kx, double ky, double xc, double yc);
edge_t scale_edge(edge_t e, double kx, double ky, double xc, double yc);
linear_figure_t scale_linear(linear_figure_t f, double kx, double ky, double xc, double yc);
point_figure_t scale_points(point_figure_t f, double kx, double ky, double xc, double yc);
object_t scale_object(object_t o, double kx, double ky, double xc, double yc);

point_t rotate_point_c(point_t p, double angle);
point_t rotate_point(point_t p, double angle, double xc, double yc);
edge_t rotate_edge(edge_t e, double angle, double xc, double yc);
linear_figure_t rotate_linear(linear_figure_t f, double angle, double xc, double yc);
point_figure_t rotate_points(point_figure_t f, double angle, double xc, double yc);
object_t rotate_object(object_t o, double angle, double xc, double yc);

#endif // OBJECTS_H
