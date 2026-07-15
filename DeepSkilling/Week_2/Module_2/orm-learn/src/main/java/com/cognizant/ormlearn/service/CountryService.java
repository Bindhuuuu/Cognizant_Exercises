package com.cognizant.ormlearn.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.cognizant.ormlearn.model.Country;
import com.cognizant.ormlearn.repository.CountryRepository;

@Service
public class CountryService {

    @Autowired
    private CountryRepository countryRepository;

    public List<Country> getAllCountries() {
        return countryRepository.findAll();
    }

    public Country getCountry(String code) {
        return countryRepository.findByCode(code).orElse(null);
    }

    @Transactional
    public void addCountry(Country country) {
        countryRepository.save(country);
    }
    
    @Transactional
    public void updateCountry(Country country) {
        countryRepository.save(country);
    }
    
    @Transactional
    public void deleteCountry(String code) {
        countryRepository.deleteById(code);
    }
    
    public List<Country> searchCountry(String text) {
        return countryRepository.findByNameContainingIgnoreCase(text);
    }
    
    public List<Country> searchCountrySorted(String text) {
        return countryRepository.findByNameContainingIgnoreCaseOrderByNameAsc(text);
    }

    public List<Country> searchCountryStartsWith(String text) {
        return countryRepository.findByNameStartingWithIgnoreCase(text);
    }

    public List<Country> searchCountryEndsWith(String text) {
        return countryRepository.findByNameEndingWithIgnoreCase(text);
    }

    public Country searchCountryExact(String name) {
        return countryRepository.findByNameIgnoreCase(name).orElse(null);
    }
}