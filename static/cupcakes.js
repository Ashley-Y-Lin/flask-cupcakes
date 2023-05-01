"use strict";

const $allCupcakesListArea = $("#all-cupcakes");
const $addCupcakeForm = $("#add-new-cupcake");


/** Display a single cupcake
 * Takes as input a single cupcake {id, flavor, size...}
*/

function displayOneCupcake(cupcake) {
  const $newCupcakeArea = $("<div>");
  const $newCupcakeImage = $("<img>").attr(
    { "src": cupcake.image_url, "alt": `An image for cupcake ${cupcake.id}` }).css("max-width", "100px");
  const $newCupcakeFlavor = $("<p>").text(cupcake.flavor);
  const $newCupcakeSize = $("<p>").text(cupcake.size);
  const $newCupcakeRating = $("<p>").text(cupcake.rating);

  $newCupcakeArea.append(
    [$newCupcakeImage, $newCupcakeFlavor, $newCupcakeSize, $newCupcakeRating]
  );

  $allCupcakesListArea.append($newCupcakeArea);
}


/** Queries the API to get the cupcakes and adds to the list on the homepage. */

async function displayAllCupcakes() {
  const response = await axios.get("/api/cupcakes");
  const cupcakes = response.data.cupcakes;

  for (let cupcake of cupcakes) {
    displayOneCupcake(cupcake);
  }
}


/** Handles form submission to let the API know about the new cupcake and
 * updates the list on the homepage to display it. */

$addCupcakeForm.on("submit", async function (event) {
  event.preventDefault();

  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  const image_url = $("#image_url").val();

  const new_cupcake = {
    flavor,
    size,
    rating,
    image_url
  };

  try {
    const response = await axios.post("/api/cupcakes", new_cupcake);

    displayOneCupcake(response.data.cupcake);
  }
  catch (error) {
    if (error.reponse) {
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    }
  }
});

displayAllCupcakes()