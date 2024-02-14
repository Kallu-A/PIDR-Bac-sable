from tdmclient import ClientAsync

import ProgLoader

if __name__ == "__main__":

    with ClientAsync(debug=0) as client:
        print(client.port)
        async def prog():
            with await client.lock() as node:
                print(node)
                error = await node.compile(ProgLoader.thymio_program)
                if error is not None:
                    print(f"Compilation error: {error['error_msg']}")
                else:
                    error = await node.run()
                    if error is not None:
                        print(f"Error {error['error_code']}")
            print("done")

        client.run_async_program(prog)