#include <SFML/Graphics.hpp>

int main() {
    // Create a 400x600 window
    sf::RenderWindow window(sf::VideoMode(sf::Vector2u(400, 600)), "Bouncing Circle");

    // Create a circle with radius 20
    sf::CircleShape circle(20.f);
    circle.setFillColor(sf::Color::Green); // Set circle color to green
    circle.setPosition(sf::Vector2f(100.f, 100.f)); // Initial position of the circle

    // Set initial speed of the circle
    sf::Vector2f speed(2.5f, 3.0f);

    // Main game loop
    while (window.isOpen()) {
        // Handle events
        while (auto event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) {
                window.close();
            }
        }

        // Move the circle
        circle.move(speed);

        // Get the current position of the circle
        sf::Vector2f position = circle.getPosition();

        // Reverse direction if the circle hits the window boundaries
        if (position.x <= 0 || position.x + 40 >= 400) { // 40 = diameter (20 * 2)
            speed.x = -speed.x; // Reverse x direction
        }
        if (position.y <= 0 || position.y + 40 >= 600) {
            speed.y = -speed.y; // Reverse y direction
        }

        // Clear the window with black color
        window.clear(sf::Color::Black);

        // Draw the circle
        window.draw(circle);

        // Display the window
        window.display();
    }

    return 0;
}