package com.cognizant.ormlearn.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cognizant.ormlearn.model.Country;

public interface CountryRepository extends JpaRepository<Country, String> {

    Optional<Country> findByCode(String code);

    // Already completed
    List<Country> findByNameContainingIgnoreCase(String text);

    // New query methods
    List<Country> findByNameContainingIgnoreCaseOrderByNameAsc(String text);

    List<Country> findByNameStartingWithIgnoreCase(String text);

    List<Country> findByNameEndingWithIgnoreCase(String text);

    Optional<Country> findByNameIgnoreCase(String name);
}