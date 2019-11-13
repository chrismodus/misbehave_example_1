Feature: The Management of users


    Scenario: Create user-broke
        Given the following user data
        | username | email                  | groups |
        | user_1   | example@example.com   |        |
        When a POST request is made to the user endpoint
        Then the user is created


    Scenario: Create and retrieve user-broke
        Given a user exists with the following user data
        | username | email                  | groups |
        | user_1   | example@example.com   |        |
        When a GET request is made to the user endpoint
        Then the user is retrieved

    