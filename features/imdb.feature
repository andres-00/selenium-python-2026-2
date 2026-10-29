Feature: IMDb movie search
  Scenario: Search Pulp Fiction and verify its rating
    Given I open IMDb home
    When I search IMDb for "Pulp Fiction" and open the first result
    Then the movie page should show a numeric rating
