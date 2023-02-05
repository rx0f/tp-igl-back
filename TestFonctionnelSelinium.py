
# Ce test fonctionnel concerne la fonctionnalitée d'ajout d'une nouvelle annonce


import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class TestFunctionnel {

    private WebDriver driver;

    @Before
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
    }

    public void testAddListing() {

        # ouvrir le site sur le navigateur, le backend doit etre lancé
        driver.get("https://tp-igl-front.vercel.app");

        # Remplir les champs
        driver.findElement(By.id("id")).sendKeys("1500");
        driver.findElement(By.id("titre")).sendKeys("Maison");
        driver.findElement(By.id("categorie")).sendKeys("Villa");
        driver.findElement(By.id("description")).sendKeys("bon etat");
        driver.findElement(By.id("surface")).sendKeys("250");
        driver.findElement(By.id("prix")).sendKeys("1000000");
        driver.findElement(By.id("localisation")).sendKeys("Alger");
        driver.findElement(By.id("utilisateur_id")).sendKeys("1440");
        driver.findElement(By.id("contact_id")).sendKeys("1540");

        driver.findElement(By.id("submit")).click();

        # Verifer si l'ajout est fait avec succés

        String expectedListingTitle = "Maison";
        String actualListingTitle = driver.findElement(By.id("listing-title")).getText();
        assertEquals(expectedListingTitle, actualListingTitle);
    }

    public void tearDown() {
        driver.quit();
    }
}



