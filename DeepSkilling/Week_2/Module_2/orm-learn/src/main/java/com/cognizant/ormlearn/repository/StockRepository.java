package com.cognizant.ormlearn.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cognizant.ormlearn.model.Stock;

public interface StockRepository extends JpaRepository<Stock, Integer> {

    List<Stock> findByDateBetween(LocalDate start, LocalDate end);

    List<Stock> findByCloseGreaterThan(double close);

    List<Stock> findTop3ByOrderByVolumeDesc();

    List<Stock> findByCodeOrderByCloseAsc(String code);

}