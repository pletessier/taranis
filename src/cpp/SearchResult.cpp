//
// Created by pletessier on 26/05/19.
//

#include "SearchResult.h"

SearchResult::SearchResult(){

    knns = new vector<vector<int64_t>*>();
    dists = new vector<vector<float>*>();

}

vector<vector<int64_t> *> *SearchResult::getKnns() const {
    return knns;
}

void SearchResult::setKnns(vector<vector<int64_t> *> *knns) {
    SearchResult::knns = knns;
}

vector<vector<float> *> *SearchResult::getDists() const {
    return dists;
}

void SearchResult::setDists(vector<vector<float> *> *dists) {
    SearchResult::dists = dists;
}
