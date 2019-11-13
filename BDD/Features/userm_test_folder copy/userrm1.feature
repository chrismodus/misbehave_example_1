Feature: The Management of users in a safe environment pfft


    Scenario: Create user
        Given the following user data
        | username | email                  | groups |
        | user_1   | example@example.com   |        |
        When a POST request is made to the user endpoint
        Then the user is created


    Scenario: Create and retrieve user
        Given a user exists with the following user data
        | username | email                  | groups |
        | user_1   | example@example.com   |        |
        When a GET request is made to the user endpoint
        Then the user is retrieved

    