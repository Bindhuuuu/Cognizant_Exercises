package com.cognizant.ormlearn.service;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cognizant.ormlearn.model.Stock;
import com.cognizant.ormlearn.repository.StockRepository;

@Service
public class StockService {

    @Autowired
    private StockRepository stockRepository;

    public List<Stock> getStocksBetween(LocalDate start, LocalDate end) {
        return stockRepository.findByDateBetween(start, end);
    }

    public List<Stock> getStocksGreaterThan(double close) {
        return stockRepository.findByCloseGreaterThan(close);
    }

    public List<Stock> getTop3Volume() {
        return stockRepository.findTop3ByOrderByVolumeDesc();
    }

    public List<Stock> getNetflixStocks() {
        return stockRepository.findByCodeOrderByCloseAsc("NFLX");
    }
}