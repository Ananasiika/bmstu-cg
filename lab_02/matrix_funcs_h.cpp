#include "matrix_funcs.h"

std::vector<double> mul(std::vector<double> v, std::vector<std::vector<double> > m) {
    std::vector<double> res;
    for (int i = 0; i < v.size(); ++i) {
        double sum = 0;
        for (int k = 0; k < v.size(); ++k) {
            sum += v[k] * m[k][i];
        }
        res.push_back(sum);
    }
    return res;
}
