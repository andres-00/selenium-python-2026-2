Feature: Global lobby
  Scenario: Enter the lobby with a unique name
    Given I open the global lobby
    When I enter the lobby with a unique username
    Then I should see that I am inside the lobby

  Scenario: Username with spaces shows an error
    Given I open the global lobby for username validation
    When I submit a username containing spaces
    Then the lobby should show the username validation error
